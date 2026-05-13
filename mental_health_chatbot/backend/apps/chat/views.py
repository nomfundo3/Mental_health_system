from django.conf import settings
from rest_framework import generics, status
from rest_framework.exceptions import NotFound
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import StreamingHttpResponse
from django.db.models import Q
import json

from apps.recommendations.models import ResourceRecommendation
from services.response_service import stream_support_response
from services.sentiment_service import assess_message

from .models import ChatMessage, ChatSession, ChatSessionFeedback, MoodCheckIn
from .serializers import (
    ChatRequestSerializer,
    ChatSessionFeedbackSerializer,
    ChatSessionSerializer,
    MoodCheckInSerializer,
)


def _build_session_title(message):
    normalized = " ".join((message or "").strip().split())
    if not normalized:
        return "Support chat"
    if len(normalized) <= 64:
        return normalized
    return f"{normalized[:59].rstrip()}....."

def _can_access_session(user, session):
    return bool(
        session
        and (
            session.user_id == user.id
            or user.is_staff
            or getattr(user, "role", "") in {"admin", "support"}
        )
    )


def _can_access_session_from_request(request, user, session):
    return bool(
        session
        and (
            (user and user.is_authenticated and _can_access_session(user, session))
            or _can_access_guest_session(request, session)
        )
    )


def _estimate_token_count(text: str) -> int:
    normalized = " ".join((text or "").split())
    if not normalized:
        return 0
    return max(1, len(normalized) // 4)


def _resource_audience_for_user(user) -> list[str]:
    if user and user.is_authenticated:
        role = getattr(user, "role", "student")
        if role in {"admin", "support"}:
            return ["all", "support"]
        return ["all", "student"]
    return ["all", "student"]


def _get_guest_session_ids(request) -> set[int]:
    raw_ids = request.session.get("guest_chat_session_ids", [])
    return {int(session_id) for session_id in raw_ids if str(session_id).isdigit()}


def _store_guest_session_id(request, session_id: int) -> None:
    session_ids = _get_guest_session_ids(request)
    session_ids.add(int(session_id))
    request.session["guest_chat_session_ids"] = sorted(session_ids)
    request.session.modified = True


def _can_access_guest_session(request, session) -> bool:
    return bool(session and session.user_id is None and session.id in _get_guest_session_ids(request))


def _get_guest_chat_usage(request) -> dict:
    token_limit = getattr(settings, "GUEST_CHAT_TOKEN_LIMIT", 2400)
    tokens_used = int(request.session.get("guest_chat_tokens_used", 0) or 0)
    return {
        "token_limit": token_limit,
        "tokens_used": tokens_used,
        "tokens_remaining": max(token_limit - tokens_used, 0),
    }


def _increment_guest_chat_usage(request, *texts: str) -> dict:
    increment = sum(_estimate_token_count(text) for text in texts)
    tokens_used = int(request.session.get("guest_chat_tokens_used", 0) or 0) + increment
    request.session["guest_chat_tokens_used"] = tokens_used
    request.session.modified = True
    token_limit = getattr(settings, "GUEST_CHAT_TOKEN_LIMIT", 2400)
    return {
        "token_limit": token_limit,
        "tokens_used": tokens_used,
        "tokens_remaining": max(token_limit - tokens_used, 0),
    }


class ChatSessionListView(generics.ListAPIView):
    serializer_class = ChatSessionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = ChatSession.objects.order_by("-updated_at")
        search_term = self.request.query_params.get("search", "").strip()

        if self.request.user.is_staff or getattr(self.request.user, "role", "") in {"admin", "support"}:
            username = self.request.query_params.get("username", "").strip()
            if username:
                queryset = queryset.filter(user__username__iexact=username)
        else:
            queryset = queryset.filter(user=self.request.user)

        if search_term:
            queryset = queryset.filter(
                Q(title__icontains=search_term)
                | Q(messages__content__icontains=search_term)
            ).distinct()

        return queryset


class ChatSessionDetailView(generics.RetrieveAPIView):
    serializer_class = ChatSessionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = ChatSession.objects.order_by("-updated_at")
        if self.request.user.is_staff or getattr(self.request.user, "role", "") in {"admin", "support"}:
            return queryset
        return queryset.filter(user=self.request.user)


class MoodCheckInCreateView(generics.ListCreateAPIView):
    serializer_class = MoodCheckInSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = MoodCheckIn.objects.filter(user=self.request.user).select_related("session").order_by("-created_at")
        session_id = self.request.query_params.get("session_id", "").strip()
        if session_id.isdigit():
            queryset = queryset.filter(session_id=int(session_id))
        return queryset

    def perform_create(self, serializer):
        if not getattr(self.request.user, "save_mood_checkins", True):
            raise PermissionDenied("Mood check-ins are currently disabled in your settings.")

        session_id = serializer.validated_data.pop("session_id", None)
        session = None
        if session_id:
            session = ChatSession.objects.filter(id=session_id).first()
            if session and not _can_access_session_from_request(self.request, self.request.user, session):
                raise PermissionDenied("You cannot attach a mood check-in to this chat session.")
        serializer.save(user=self.request.user, session=session)


class ChatSessionFeedbackUpsertView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = ChatSessionFeedbackSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        session_id = serializer.validated_data["session_id"]
        session = ChatSession.objects.filter(id=session_id).first()
        if session is None:
            raise NotFound("Chat session not found.")

        user = request.user
        is_authenticated = bool(user and user.is_authenticated)

        if is_authenticated:
            if not _can_access_session_from_request(request, user, session):
                raise PermissionDenied("You cannot leave feedback for this chat session.")
        elif not _can_access_guest_session(request, session):
            raise PermissionDenied("You cannot leave feedback for this guest chat session.")

        feedback, created = ChatSessionFeedback.objects.update_or_create(
            session=session,
            defaults={
                "user": user if is_authenticated else None,
                "rating": serializer.validated_data["rating"],
                "comments": serializer.validated_data.get("comments", ""),
            },
        )

        response_serializer = ChatSessionFeedbackSerializer(feedback)
        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK,
        )


class ChatConversationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = ChatRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        message = serializer.validated_data["message"]
        session_id = serializer.validated_data.get("session_id")
        user = request.user
        is_authenticated = bool(user and user.is_authenticated)

        session = ChatSession.objects.filter(id=session_id).first() if session_id else None
        if session is not None:
            if not _can_access_session_from_request(request, user, session):
                if is_authenticated:
                    raise PermissionDenied("You cannot continue a chat session that does not belong to you.")
                raise PermissionDenied("You cannot continue a guest chat session that does not belong to you.")

        if not is_authenticated:
            guest_usage = _get_guest_chat_usage(request)
            projected_message_cost = _estimate_token_count(message)
            if guest_usage["tokens_remaining"] < projected_message_cost:
                return Response(
                    {
                        "detail": "Guest chat limit reached. Log in to continue chatting.",
                        "guest_chat": guest_usage,
                    },
                    status=status.HTTP_429_TOO_MANY_REQUESTS,
                )

        persist_chat_history = bool(is_authenticated and getattr(user, "save_chat_history", True))

        if session is None:
            session = ChatSession.objects.create(user=user if persist_chat_history else None)
            if not persist_chat_history:
                _store_guest_session_id(request, session.id)

        assessment = assess_message(message)
        user_message = ChatMessage.objects.create(
            session=session,
            role="user",
            content=message,
            sentiment=assessment["sentiment"],
            risk_level=assessment["risk_level"],
            detected_categories=assessment["resource_categories"],
            flagged=assessment["flagged"],
            confidence_score=assessment.get("confidence_score"),
            source="rule_engine",
        )

        if not session.title or session.title == "Support chat":
            session.title = _build_session_title(message)

        resources = list(
            ResourceRecommendation.objects.filter(
                category__in=assessment["resource_categories"],
                is_active=True,
                audience__in=_resource_audience_for_user(user),
            )
            .order_by("-is_emergency", "-priority", "title")
            .values(
                "title",
                "description",
                "url",
                "category",
                "audience",
                "priority",
                "is_emergency",
            )
        )

        def generate_stream():
            content_parts = []
            response_source = "fallback"
            fallback_used = True
            guest_usage_data = _get_guest_chat_usage(request) if not is_authenticated else None
            assistant_message = ChatMessage.objects.create(
                session=session,
                role="assistant",
                content="",
                sentiment="neutral",
                risk_level=assessment["risk_level"],
                detected_categories=assessment["resource_categories"],
                flagged=False,
                confidence_score=assessment.get("confidence_score"),
                fallback_used=fallback_used,
                source=response_source,
            )

            for chunk_payload in stream_support_response(
                message=message,
                assessment=assessment,
                resources=resources,
                user=user if is_authenticated else None,
            ):
                chunk_content = chunk_payload["content"]
                response_source = chunk_payload["source"]
                fallback_used = chunk_payload["fallback_used"]

                if chunk_content:
                    content_parts.append(chunk_content)
                    assistant_message.content = "".join(content_parts)
                    assistant_message.fallback_used = fallback_used
                    assistant_message.source = response_source
                    assistant_message.save(update_fields=["content", "fallback_used", "source"])
                    yield json.dumps({"type": "content", "data": chunk_content}) + "\n"

            assistant_content = "".join(content_parts).strip()
            if not is_authenticated:
                guest_usage_data = _increment_guest_chat_usage(request, message, assistant_content)

            assistant_message.content = assistant_content
            assistant_message.fallback_used = fallback_used
            assistant_message.source = response_source
            assistant_message.save(
                update_fields=[
                    "content",
                    "fallback_used",
                    "source",
                ]
            )

            session.last_message_at = assistant_message.created_at
            session.last_risk_level = assessment["risk_level"]
            session.escalation_required = assessment["flagged"]
            if assessment["risk_level"] == "high":
                session.status = "escalated"
            elif assessment["flagged"]:
                session.status = "flagged"
            else:
                session.status = "active"
            session.save(
                update_fields=[
                    "last_message_at",
                    "last_risk_level",
                    "escalation_required",
                    "status",
                    "title",
                    "updated_at",
                ]
            )

            session.refresh_from_db()

            final_data = {
                "type": "complete",
                "session": ChatSessionSerializer(session).data,
                "assessment": assessment,
                "resources": resources,
                "response_source": response_source,
            }
            if guest_usage_data is not None:
                final_data["guest_chat"] = guest_usage_data
            yield json.dumps(final_data) + "\n"
        
        response = StreamingHttpResponse(
            generate_stream(),
            content_type="application/x-ndjson"
        )
        response["Cache-Control"] = "no-cache"
        response["X-Accel-Buffering"] = "no"
        return response

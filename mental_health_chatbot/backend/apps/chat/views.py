from rest_framework import generics
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.http import StreamingHttpResponse
import json

from apps.recommendations.models import ResourceRecommendation
from services.response_service import stream_support_response
from services.sentiment_service import assess_message

from .models import ChatMessage, ChatSession, MoodCheckIn
from .serializers import (
    ChatRequestSerializer,
    ChatSessionSerializer,
    MoodCheckInSerializer,
)


def _build_session_title(message):
    normalized = " ".join((message or "").strip().split())
    if not normalized:
        return "Support chat"
    if len(normalized) <= 42:
        return normalized
    return f"{normalized[:37].rstrip()}....."

def _can_access_session(user, session):
    return bool(
        session
        and (
            session.user_id == user.id
            or user.is_staff
            or getattr(user, "role", "") in {"admin", "support"}
        )
    )


class ChatSessionListView(generics.ListAPIView):
    serializer_class = ChatSessionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = ChatSession.objects.order_by("-updated_at")
        if self.request.user.is_staff or getattr(self.request.user, "role", "") in {"admin", "support"}:
            username = self.request.query_params.get("username", "").strip()
            if username:
                return queryset.filter(user__username__iexact=username)
            return queryset

        return queryset.filter(user=self.request.user)


class ChatSessionDetailView(generics.RetrieveAPIView):
    serializer_class = ChatSessionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = ChatSession.objects.order_by("-updated_at")
        if self.request.user.is_staff or getattr(self.request.user, "role", "") in {"admin", "support"}:
            return queryset
        return queryset.filter(user=self.request.user)


class MoodCheckInCreateView(generics.CreateAPIView):
    queryset = MoodCheckIn.objects.all()
    serializer_class = MoodCheckInSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        session_id = serializer.validated_data.pop("session_id", None)
        session = None
        if session_id:
            session = ChatSession.objects.filter(id=session_id).first()
            if session and not _can_access_session(self.request.user, session):
                raise PermissionDenied("You cannot attach a mood check-in to this chat session.")
        serializer.save(user=self.request.user, session=session)


class ChatConversationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = ChatRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        message = serializer.validated_data["message"]
        session_id = serializer.validated_data.get("session_id")
        user = request.user

        session = ChatSession.objects.filter(id=session_id).first() if session_id else None
        if session is not None and not _can_access_session(user, session):
            raise PermissionDenied("You cannot continue a chat session that does not belong to you.")
        if session is None:
            session = ChatSession.objects.create(user=user)

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

            for chunk_payload in stream_support_response(
                message=message,
                assessment=assessment,
                resources=resources,
                user=user,
            ):
                chunk_content = chunk_payload["content"]
                response_source = chunk_payload["source"]
                fallback_used = chunk_payload["fallback_used"]

                if chunk_content:
                    content_parts.append(chunk_content)
                    yield json.dumps({"type": "content", "data": chunk_content}) + "\n"

            assistant_content = "".join(content_parts).strip()

            ChatMessage.objects.create(
                session=session,
                role="assistant",
                content=assistant_content,
                sentiment="neutral",
                risk_level=assessment["risk_level"],
                detected_categories=assessment["resource_categories"],
                flagged=False,
                confidence_score=assessment.get("confidence_score"),
                fallback_used=fallback_used,
                source=response_source,
            )

            session.last_message_at = user_message.created_at
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
            yield json.dumps(final_data) + "\n"
        
        response = StreamingHttpResponse(
            generate_stream(),
            content_type="application/x-ndjson"
        )
        response["Cache-Control"] = "no-cache"
        response["X-Accel-Buffering"] = "no"
        return response

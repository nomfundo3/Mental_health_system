from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.recommendations.models import ResourceRecommendation
from services.response_service import build_support_response
from services.sentiment_service import assess_message

from .models import ChatMessage, ChatSession, MoodCheckIn
from .serializers import (
    ChatRequestSerializer,
    ChatSessionSerializer,
    MoodCheckInSerializer,
)

User = get_user_model()


class ChatSessionListView(generics.ListAPIView):
    queryset = ChatSession.objects.all().order_by("-updated_at")
    serializer_class = ChatSessionSerializer


class MoodCheckInCreateView(generics.CreateAPIView):
    queryset = MoodCheckIn.objects.all()
    serializer_class = MoodCheckInSerializer


class ChatConversationView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = ChatRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        message = serializer.validated_data["message"]
        session_id = serializer.validated_data.get("session_id")
        username = serializer.validated_data.get("username", "").strip()

        user = User.objects.filter(username=username).first() if username else None
        session = ChatSession.objects.filter(id=session_id).first() if session_id else None
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

        resources = list(
            ResourceRecommendation.objects.filter(
                category__in=assessment["resource_categories"],
                is_active=True,
            )
            .order_by("-priority", "title")
            .values(
                "title", "description", "url", "category", "audience", "priority"
            )
        )

        response_text = build_support_response(message=message, assessment=assessment, resources=resources)
        fallback_used = assessment["risk_level"] == "high"
        ChatMessage.objects.create(
            session=session,
            role="assistant",
            content=response_text,
            sentiment="neutral",
            risk_level=assessment["risk_level"],
            detected_categories=assessment["resource_categories"],
            flagged=False,
            confidence_score=assessment.get("confidence_score"),
            fallback_used=fallback_used,
            source="fallback" if fallback_used else "rule_engine",
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
                "updated_at",
            ]
        )

        session.refresh_from_db()
        return Response(
            {
                "session": ChatSessionSerializer(session).data,
                "assessment": assessment,
                "resources": resources,
            },
            status=status.HTTP_200_OK,
        )

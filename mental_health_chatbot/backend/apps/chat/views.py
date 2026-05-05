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
        ChatMessage.objects.create(
            session=session,
            role="user",
            content=message,
            sentiment=assessment["sentiment"],
            risk_level=assessment["risk_level"],
            flagged=assessment["flagged"],
        )

        resources = list(
            ResourceRecommendation.objects.filter(category__in=assessment["resource_categories"]).values(
                "title", "description", "url", "category"
            )
        )

        response_text = build_support_response(message=message, assessment=assessment, resources=resources)
        ChatMessage.objects.create(
            session=session,
            role="assistant",
            content=response_text,
            sentiment=assessment["sentiment"],
            risk_level=assessment["risk_level"],
            flagged=assessment["flagged"],
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

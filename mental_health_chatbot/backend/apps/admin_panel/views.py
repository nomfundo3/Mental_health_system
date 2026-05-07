from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from apps.chat.models import ChatMessage
from apps.chat.models import ChatSession, MoodCheckIn
from apps.recommendations.models import ResourceRecommendation

from .permissions import IsSupportOrAdmin


class FlaggedMessagesView(APIView):
    permission_classes = [IsAuthenticated, IsSupportOrAdmin]

    def get(self, request, *args, **kwargs):
        flagged = ChatMessage.objects.filter(flagged=True).order_by("-created_at")[:20]
        data = [
            {
                "id": message.id,
                "session_id": message.session_id,
                "content": message.content,
                "risk_level": message.risk_level,
                "sentiment": message.sentiment,
                "detected_categories": message.detected_categories,
                "created_at": message.created_at,
            }
            for message in flagged
        ]
        return Response({"flagged_messages": data})


class AdminDashboardView(APIView):
    permission_classes = [IsAuthenticated, IsSupportOrAdmin]

    def get(self, request, *args, **kwargs):
        return Response(
            {
                "totals": {
                    "users": request.user.__class__.objects.count(),
                    "sessions": ChatSession.objects.count(),
                    "messages": ChatMessage.objects.count(),
                    "mood_checkins": MoodCheckIn.objects.count(),
                    "resources": ResourceRecommendation.objects.filter(is_active=True).count(),
                    "flagged_messages": ChatMessage.objects.filter(flagged=True).count(),
                },
                "latest_flagged": [
                    {
                        "id": message.id,
                        "session_id": message.session_id,
                        "risk_level": message.risk_level,
                        "content": message.content,
                        "created_at": message.created_at,
                    }
                    for message in ChatMessage.objects.filter(flagged=True).order_by("-created_at")[:5]
                ],
            }
        )

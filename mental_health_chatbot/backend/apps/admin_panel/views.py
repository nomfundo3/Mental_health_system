from django.contrib.auth import get_user_model
from django.db.models import Avg, Count
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from apps.chat.models import ChatMessage
from apps.chat.models import ChatSession, MoodCheckIn
from apps.recommendations.models import ResourceRecommendation

from .permissions import IsSupportOrAdmin

User = get_user_model()


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
        session_statuses = {
            item["status"]: item["total"]
            for item in ChatSession.objects.values("status").annotate(total=Count("id"))
        }
        risk_levels = {
            item["risk_level"]: item["total"]
            for item in ChatMessage.objects.filter(role="user").values("risk_level").annotate(total=Count("id"))
        }
        moods = {
            item["mood"]: item["total"]
            for item in MoodCheckIn.objects.values("mood").annotate(total=Count("id"))
        }

        return Response(
            {
                "totals": {
                    "users": User.objects.count(),
                    "sessions": ChatSession.objects.count(),
                    "messages": ChatMessage.objects.count(),
                    "mood_checkins": MoodCheckIn.objects.count(),
                    "resources": ResourceRecommendation.objects.filter(is_active=True).count(),
                    "flagged_messages": ChatMessage.objects.filter(flagged=True).count(),
                    "escalated_sessions": ChatSession.objects.filter(status="escalated").count(),
                    "active_sessions": ChatSession.objects.filter(status="active").count(),
                    "fallback_messages": ChatMessage.objects.filter(fallback_used=True).count(),
                    "reviewed_flagged": ChatMessage.objects.filter(flagged=True, reviewed_by_admin=True).count(),
                },
                "breakdowns": {
                    "session_statuses": {
                        "active": session_statuses.get("active", 0),
                        "flagged": session_statuses.get("flagged", 0),
                        "escalated": session_statuses.get("escalated", 0),
                        "closed": session_statuses.get("closed", 0),
                    },
                    "risk_levels": {
                        "low": risk_levels.get("low", 0),
                        "medium": risk_levels.get("medium", 0),
                        "high": risk_levels.get("high", 0),
                    },
                    "moods": {
                        "great": moods.get("great", 0),
                        "okay": moods.get("okay", 0),
                        "stressed": moods.get("stressed", 0),
                        "anxious": moods.get("anxious", 0),
                        "overwhelmed": moods.get("overwhelmed", 0),
                    },
                },
                "insights": {
                    "average_stress_level": MoodCheckIn.objects.aggregate(avg=Avg("stress_level"))["avg"] or 0,
                    "unreviewed_flagged": ChatMessage.objects.filter(flagged=True, reviewed_by_admin=False).count(),
                    "high_risk_messages": ChatMessage.objects.filter(role="user", risk_level="high").count(),
                    "support_resources": ResourceRecommendation.objects.filter(
                        is_active=True,
                        audience__in=["all", "support"],
                    ).count(),
                },
                "latest_flagged": [
                    {
                        "id": message.id,
                        "session_id": message.session_id,
                        "session_title": message.session.title,
                        "username": message.session.user.username if message.session.user else "Anonymous",
                        "risk_level": message.risk_level,
                        "sentiment": message.sentiment,
                        "detected_categories": message.detected_categories,
                        "content": message.content,
                        "created_at": message.created_at,
                        "reviewed_by_admin": message.reviewed_by_admin,
                    }
                    for message in ChatMessage.objects.filter(flagged=True).order_by("-created_at")[:5]
                ],
                "recent_sessions": [
                    {
                        "id": session.id,
                        "title": session.title,
                        "username": session.user.username if session.user else "Anonymous",
                        "status": session.status,
                        "last_risk_level": session.last_risk_level,
                        "message_count": session.messages.count(),
                        "updated_at": session.updated_at,
                    }
                    for session in ChatSession.objects.select_related("user").order_by("-updated_at")[:6]
                ],
                "recent_mood_checkins": [
                    {
                        "id": checkin.id,
                        "username": checkin.user.username if checkin.user else "Anonymous",
                        "session_id": checkin.session_id,
                        "mood": checkin.mood,
                        "stress_level": checkin.stress_level,
                        "notes": checkin.notes,
                        "created_at": checkin.created_at,
                    }
                    for checkin in MoodCheckIn.objects.select_related("user", "session").order_by("-created_at")[:6]
                ],
            }
        )

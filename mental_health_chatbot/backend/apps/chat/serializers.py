from rest_framework import serializers

from .models import ChatMessage, ChatSession, MoodCheckIn


class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = [
            "id",
            "role",
            "content",
            "sentiment",
            "risk_level",
            "detected_categories",
            "flagged",
            "confidence_score",
            "fallback_used",
            "source",
            "reviewed_by_admin",
            "reviewed_at",
            "created_at",
        ]
        read_only_fields = fields


class ChatSessionSerializer(serializers.ModelSerializer):
    messages = ChatMessageSerializer(many=True, read_only=True)

    class Meta:
        model = ChatSession
        fields = [
            "id",
            "title",
            "status",
            "last_message_at",
            "last_risk_level",
            "escalation_required",
            "notes",
            "created_at",
            "updated_at",
            "messages",
        ]
        read_only_fields = fields


class MoodCheckInSerializer(serializers.ModelSerializer):
    class Meta:
        model = MoodCheckIn
        fields = ["id", "user", "session", "mood", "notes", "stress_level", "created_at"]
        read_only_fields = ["id", "created_at"]


class ChatRequestSerializer(serializers.Serializer):
    session_id = serializers.IntegerField(required=False)
    message = serializers.CharField()
    username = serializers.CharField(required=False, allow_blank=True)

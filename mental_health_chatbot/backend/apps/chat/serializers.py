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
    session_id = serializers.IntegerField(required=False, write_only=True)
    stress_level = serializers.IntegerField(required=False)

    class Meta:
        model = MoodCheckIn
        fields = [
            "id",
            "user",
            "session",
            "session_id",
            "mood",
            "notes",
            "stress_level",
            "created_at",
        ]
        read_only_fields = ["id", "user", "session", "created_at"]


class ChatRequestSerializer(serializers.Serializer):
    session_id = serializers.IntegerField(required=False, allow_null=True)
    message = serializers.CharField(required=True, allow_blank=False)

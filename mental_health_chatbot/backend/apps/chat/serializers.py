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
            "flagged",
            "created_at",
        ]
        read_only_fields = fields


class ChatSessionSerializer(serializers.ModelSerializer):
    messages = ChatMessageSerializer(many=True, read_only=True)

    class Meta:
        model = ChatSession
        fields = ["id", "title", "created_at", "updated_at", "messages"]
        read_only_fields = fields


class MoodCheckInSerializer(serializers.ModelSerializer):
    class Meta:
        model = MoodCheckIn
        fields = ["id", "user", "mood", "notes", "created_at"]
        read_only_fields = ["id", "created_at"]


class ChatRequestSerializer(serializers.Serializer):
    session_id = serializers.IntegerField(required=False)
    message = serializers.CharField()
    username = serializers.CharField(required=False, allow_blank=True)

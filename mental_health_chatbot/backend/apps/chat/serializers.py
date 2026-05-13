from rest_framework import serializers

from .models import ChatMessage, ChatSession, ChatSessionFeedback, MoodCheckIn


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


class ChatSessionFeedbackSerializer(serializers.ModelSerializer):
    session_id = serializers.IntegerField(write_only=True, required=True)

    class Meta:
        model = ChatSessionFeedback
        fields = [
            "id",
            "session_id",
            "session",
            "user",
            "rating",
            "comments",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "session", "user", "created_at", "updated_at"]


class ChatSessionSerializer(serializers.ModelSerializer):
    messages = ChatMessageSerializer(many=True, read_only=True)
    title = serializers.SerializerMethodField()
    feedback = ChatSessionFeedbackSerializer(read_only=True)

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
            "feedback",
        ]
        read_only_fields = fields

    def get_title(self, obj):
        title = (obj.title or "").strip()
        if title and title != "Support chat":
            return title

        first_user_message = obj.messages.filter(role="user").order_by("created_at").first()
        if first_user_message and first_user_message.content:
            normalized = " ".join(first_user_message.content.strip().split())
            if len(normalized) <= 64:
                return normalized
            return f"{normalized[:59].rstrip()}....."

        return title or "Support chat"


class MoodCheckInSerializer(serializers.ModelSerializer):
    session_id = serializers.IntegerField(required=False, write_only=True)
    stress_level = serializers.IntegerField(required=False)
    session_title = serializers.SerializerMethodField()

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
            "session_title",
        ]
        read_only_fields = ["id", "user", "session", "created_at"]

    def validate_stress_level(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Stress level must be between 1 and 5.")
        return value

    def get_session_title(self, obj):
        if obj.session and obj.session.title:
            return obj.session.title
        return ""


class ChatRequestSerializer(serializers.Serializer):
    session_id = serializers.IntegerField(required=False, allow_null=True)
    message = serializers.CharField(required=True, allow_blank=False)

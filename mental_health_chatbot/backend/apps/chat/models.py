from django.conf import settings
from django.db import models


class ChatSession(models.Model):
    STATUS_CHOICES = [
        ("active", "Active"),
        ("closed", "Closed"),
        ("flagged", "Flagged"),
        ("escalated", "Escalated"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="chat_sessions",
    )
    title = models.CharField(max_length=255, default="Support chat")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")
    last_message_at = models.DateTimeField(null=True, blank=True)
    last_risk_level = models.CharField(max_length=20, default="low")
    escalation_required = models.BooleanField(default=False)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.title} ({self.pk})"


class ChatMessage(models.Model):
    ROLE_CHOICES = [
        ("user", "User"),
        ("assistant", "Assistant"),
        ("system", "System"),
    ]
    SENTIMENT_CHOICES = [
        ("positive", "Positive"),
        ("neutral", "Neutral"),
        ("negative", "Negative"),
    ]
    RISK_LEVEL_CHOICES = [
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
    ]
    SOURCE_CHOICES = [
        ("rule_engine", "Rule Engine"),
        ("ai_service", "AI Service"),
        ("fallback", "Fallback"),
        ("human", "Human"),
    ]

    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name="messages")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    content = models.TextField()
    sentiment = models.CharField(max_length=20, choices=SENTIMENT_CHOICES, default="neutral")
    risk_level = models.CharField(max_length=20, choices=RISK_LEVEL_CHOICES, default="low")
    detected_categories = models.JSONField(default=list, blank=True)
    flagged = models.BooleanField(default=False)
    confidence_score = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    fallback_used = models.BooleanField(default=False)
    source = models.CharField(max_length=20, choices=SOURCE_CHOICES, default="rule_engine")
    reviewed_by_admin = models.BooleanField(default=False)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]


class MoodCheckIn(models.Model):
    MOOD_CHOICES = [
        ("great", "Great"),
        ("okay", "Okay"),
        ("stressed", "Stressed"),
        ("anxious", "Anxious"),
        ("overwhelmed", "Overwhelmed"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="mood_check_ins",
    )
    session = models.ForeignKey(
        ChatSession,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="mood_check_ins",
    )
    mood = models.CharField(max_length=20, choices=MOOD_CHOICES)
    notes = models.TextField(blank=True)
    stress_level = models.PositiveSmallIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

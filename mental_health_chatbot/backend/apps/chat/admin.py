from django.contrib import admin

from .models import ChatMessage, ChatSession, MoodCheckIn


@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "user", "status", "last_risk_level", "escalation_required", "updated_at")
    list_filter = ("status", "last_risk_level", "escalation_required")
    search_fields = ("title", "user__username", "user__display_name")


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ("id", "session", "role", "risk_level", "flagged", "fallback_used", "created_at")
    list_filter = ("role", "risk_level", "flagged", "fallback_used", "source")
    search_fields = ("content", "session__title", "session__user__username")


@admin.register(MoodCheckIn)
class MoodCheckInAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "mood", "stress_level", "created_at")
    list_filter = ("mood", "stress_level")
    search_fields = ("user__username", "notes")

from django.urls import path

from .views import ChatConversationView, ChatSessionDetailView, ChatSessionListView, MoodCheckInCreateView


urlpatterns = [
    path("sessions/", ChatSessionListView.as_view(), name="chat-sessions"),
    path("sessions/<int:pk>/", ChatSessionDetailView.as_view(), name="chat-session-detail"),
    path("message/", ChatConversationView.as_view(), name="chat-message"),
    path("mood-checkins/", MoodCheckInCreateView.as_view(), name="mood-checkin"),
]

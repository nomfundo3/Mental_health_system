from django.urls import path

from .views import ChatConversationView, ChatSessionListView, MoodCheckInCreateView


urlpatterns = [
    path("sessions/", ChatSessionListView.as_view(), name="chat-sessions"),
    path("message/", ChatConversationView.as_view(), name="chat-message"),
    path("mood-checkins/", MoodCheckInCreateView.as_view(), name="mood-checkin"),
]

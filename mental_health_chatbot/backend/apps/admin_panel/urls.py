from django.urls import path

from .views import AdminDashboardView, FlaggedMessagesView


urlpatterns = [
    path("dashboard/", AdminDashboardView.as_view(), name="admin-dashboard"),
    path("flagged-messages/", FlaggedMessagesView.as_view(), name="flagged-messages"),
]

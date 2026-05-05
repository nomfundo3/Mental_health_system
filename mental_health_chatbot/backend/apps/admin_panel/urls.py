from django.urls import path

from .views import FlaggedMessagesView


urlpatterns = [
    path("flagged-messages/", FlaggedMessagesView.as_view(), name="flagged-messages"),
]

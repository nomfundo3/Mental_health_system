from django.urls import path

from .views import AiHealthView


urlpatterns = [
    path("health/", AiHealthView.as_view(), name="ai-health"),
]

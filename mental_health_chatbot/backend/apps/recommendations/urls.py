from django.urls import path

from .views import ResourceRecommendationListView


urlpatterns = [
    path("", ResourceRecommendationListView.as_view(), name="resource-list"),
]

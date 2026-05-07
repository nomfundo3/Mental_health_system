from rest_framework import generics

from .models import ResourceRecommendation
from .serializers import ResourceRecommendationSerializer


class ResourceRecommendationListView(generics.ListAPIView):
    serializer_class = ResourceRecommendationSerializer

    def get_queryset(self):
        queryset = ResourceRecommendation.objects.filter(is_active=True).order_by(
            "-is_emergency", "-priority", "title"
        )
        category = self.request.query_params.get("category", "").strip()
        if category:
            queryset = queryset.filter(category=category)
        return queryset

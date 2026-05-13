from rest_framework import generics

from .models import ResourceRecommendation
from .serializers import ResourceRecommendationSerializer


class ResourceRecommendationListView(generics.ListAPIView):
    serializer_class = ResourceRecommendationSerializer

    def get_queryset(self):
        audience = ["all", "student"]
        user = getattr(self.request, "user", None)
        if user and user.is_authenticated and getattr(user, "role", "") in {"admin", "support"}:
            audience = ["all", "support"]

        queryset = ResourceRecommendation.objects.filter(
            is_active=True,
            audience__in=audience,
        ).order_by(
            "-is_emergency", "-priority", "title"
        )
        category = self.request.query_params.get("category", "").strip()
        if category:
            queryset = queryset.filter(category=category)
        return queryset

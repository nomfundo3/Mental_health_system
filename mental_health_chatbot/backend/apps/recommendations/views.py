from rest_framework import generics

from .models import ResourceRecommendation
from .serializers import ResourceRecommendationSerializer


class ResourceRecommendationListView(generics.ListAPIView):
    queryset = ResourceRecommendation.objects.all()
    serializer_class = ResourceRecommendationSerializer

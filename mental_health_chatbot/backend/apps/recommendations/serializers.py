from rest_framework import serializers

from .models import ResourceRecommendation


class ResourceRecommendationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResourceRecommendation
        fields = ["id", "title", "description", "url", "category", "is_emergency"]

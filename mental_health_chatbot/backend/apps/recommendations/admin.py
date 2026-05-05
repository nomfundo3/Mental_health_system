from django.contrib import admin

from .models import ResourceRecommendation


@admin.register(ResourceRecommendation)
class ResourceRecommendationAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "audience", "priority", "is_active", "is_emergency")
    list_filter = ("category", "audience", "is_active", "is_emergency")
    search_fields = ("title", "description")

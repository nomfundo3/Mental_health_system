from django.db import models


class ResourceRecommendation(models.Model):
    CATEGORY_CHOICES = [
        ("general", "General"),
        ("anxiety", "Anxiety"),
        ("stress", "Stress"),
        ("crisis", "Crisis"),
    ]
    AUDIENCE_CHOICES = [
        ("all", "All"),
        ("student", "Student"),
        ("support", "Support"),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    url = models.URLField(blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default="general")
    audience = models.CharField(max_length=20, choices=AUDIENCE_CHOICES, default="all")
    tags = models.JSONField(default=list, blank=True)
    priority = models.PositiveSmallIntegerField(default=1)
    is_active = models.BooleanField(default=True)
    is_emergency = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.title

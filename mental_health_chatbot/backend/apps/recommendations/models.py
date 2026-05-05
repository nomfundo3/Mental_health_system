from django.db import models


class ResourceRecommendation(models.Model):
    CATEGORY_CHOICES = [
        ("general", "General"),
        ("anxiety", "Anxiety"),
        ("stress", "Stress"),
        ("crisis", "Crisis"),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    url = models.URLField(blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default="general")
    is_emergency = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.title

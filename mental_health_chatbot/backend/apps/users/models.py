from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = [
        ("student", "Student"),
        ("admin", "Admin"),
        ("support", "Support"),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="student")
    display_name = models.CharField(max_length=150, blank=True)
    preferred_language = models.CharField(max_length=20, default="en")
    consent_accepted = models.BooleanField(default=False)
    consent_accepted_at = models.DateTimeField(null=True, blank=True)
    emergency_contact_opt_in = models.BooleanField(default=False)
    is_anonymous = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.display_name or self.username

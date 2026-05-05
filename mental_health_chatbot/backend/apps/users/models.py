from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = [
        ("student", "Student"),
        ("admin", "Admin"),
        ("support", "Support"),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="student")
    consent_accepted = models.BooleanField(default=False)
    emergency_contact_opt_in = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.username

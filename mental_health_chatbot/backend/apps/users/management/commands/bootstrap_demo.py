from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

User = get_user_model()


class Command(BaseCommand):
    help = "Create ready-to-use demo users for student and admin presentation flows."

    def handle(self, *args, **options):
        demo_users = [
            {
                "username": "studentdemo",
                "email": "studentdemo@example.com",
                "password": "StrongPass123!",
                "display_name": "Student Demo",
                "role": "student",
                "consent_accepted": True,
            },
            {
                "username": "supportdemo",
                "email": "supportdemo@example.com",
                "password": "StrongPass123!",
                "display_name": "Support Demo",
                "role": "admin",
                "consent_accepted": True,
                "is_staff": True,
                "is_superuser": True,
            },
        ]

        for payload in demo_users:
            password = payload.pop("password")
            user, created = User.objects.get_or_create(
                username=payload["username"],
                defaults=payload,
            )
            if created:
                user.set_password(password)
                user.save()
                self.stdout.write(self.style.SUCCESS(f"Created {user.username}"))
            else:
                updated = False
                for field, value in payload.items():
                    if getattr(user, field) != value:
                        setattr(user, field, value)
                        updated = True
                user.set_password(password)
                user.save()
                status = "Updated" if updated else "Reset password for"
                self.stdout.write(self.style.WARNING(f"{status} {user.username}"))

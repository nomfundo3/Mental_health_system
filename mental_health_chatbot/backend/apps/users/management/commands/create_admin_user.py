from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.core.management.base import CommandError
import os

User = get_user_model()


class Command(BaseCommand):
    help = "Create an admin user with the correct role and permissions."

    def add_arguments(self, parser):
        parser.add_argument("--username", type=str, help="Username for the new admin")
        parser.add_argument("--email", type=str, help="Email for the new admin")
        parser.add_argument("--password", type=str, help="Password for the new admin")
        parser.add_argument("--display_name", type=str, default="", help="Display name for the new admin")

    def handle(self, *args, **options):
        username = options["username"] or os.environ.get("ADMIN_USERNAME")
        email = options["email"] or os.environ.get("ADMIN_EMAIL")
        password = options["password"] or os.environ.get("ADMIN_PASSWORD")
        display_name = options["display_name"] or os.environ.get("ADMIN_DISPLAY_NAME") or username

        missing = [
            name
            for name, value in {
                "ADMIN_USERNAME": username,
                "ADMIN_EMAIL": email,
                "ADMIN_PASSWORD": password,
            }.items()
            if not value
        ]
        if missing:
            raise CommandError(f"Missing admin configuration: {', '.join(missing)}")

        user = User.objects.filter(username=username).first() or User.objects.filter(email__iexact=email).first()

        if user is None:
            user = User.objects.create_superuser(
                username=username,
                email=email,
                password=password,
                display_name=display_name,
                role="admin",
                consent_accepted=True,
            )
            self.stdout.write(self.style.SUCCESS(f"Successfully created superuser: {username}"))
            return

        user.username = username
        user.email = email
        user.display_name = display_name
        user.role = "admin"
        user.is_staff = True
        user.is_superuser = True
        user.consent_accepted = True
        user.set_password(password)
        user.save()

        self.stdout.write(self.style.SUCCESS(f"Successfully updated superuser: {username}"))

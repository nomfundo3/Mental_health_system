from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

User = get_user_model()


class Command(BaseCommand):
    help = "Create an admin user with the correct role and permissions."

    def add_arguments(self, parser):
        parser.add_argument("--username", type=str, required=True, help="Username for the new admin")
        parser.add_argument("--email", type=str, required=True, help="Email for the new admin")
        parser.add_argument("--password", type=str, required=True, help="Password for the new admin")
        parser.add_argument("--display_name", type=str, default="", help="Display name for the new admin")

    def handle(self, *args, **options):
        username = options["username"]
        email = options["email"]
        password = options["password"]
        display_name = options["display_name"] or username

        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.ERROR(f"User with username '{username}' already exists."))
            return

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            display_name=display_name,
            role="admin",
            is_staff=False,
            is_superuser=False,
            consent_accepted=True
        )

        self.stdout.write(self.style.SUCCESS(f"Successfully created browser admin user: {username}"))

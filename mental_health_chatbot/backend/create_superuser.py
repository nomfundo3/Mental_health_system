import os

import django


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.contrib.auth import get_user_model  # noqa: E402


User = get_user_model()

username = os.environ.get("ADMIN_USERNAME", "mbalenhle")
email = os.environ.get("ADMIN_EMAIL", "mbalenhle@epftechhubic.org")
password = os.environ.get("ADMIN_PASSWORD")
display_name = os.environ.get("ADMIN_DISPLAY_NAME", "Mbalenhle")

if not password:
    raise RuntimeError("ADMIN_PASSWORD must be set in Render environment variables.")

user = User.objects.filter(username=username).first() or User.objects.filter(email__iexact=email).first()

if user is None:
    User.objects.create_superuser(
        username=username,
        email=email,
        password=password,
        display_name=display_name,
        role="admin",
        consent_accepted=True,
    )
    print("Superuser created")
else:
    user.username = username
    user.email = email
    user.display_name = display_name
    user.role = "admin"
    user.is_staff = True
    user.is_superuser = True
    user.consent_accepted = True
    user.set_password(password)
    user.save()
    print("Superuser updated")

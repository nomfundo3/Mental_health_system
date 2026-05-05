from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "role", "consent_accepted", "is_staff")
    list_filter = ("role", "consent_accepted", "is_staff")

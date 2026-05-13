from rest_framework.permissions import BasePermission


class IsSupportOrAdmin(BasePermission):
    message = "You do not have permission to access the admin support panel."

    def has_permission(self, request, view):
        user = request.user
        return bool(
            user
            and user.is_authenticated
            and (user.is_staff or getattr(user, "role", "") in {"admin", "support"})
        )


class IsSuperuserOnly(BasePermission):
    message = "You do not have permission to access the superuser dashboard."

    def has_permission(self, request, view):
        user = request.user
        return bool(user and user.is_authenticated and user.is_superuser)

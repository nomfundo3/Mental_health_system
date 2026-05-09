from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.views.decorators.csrf import ensure_csrf_cookie
from django.shortcuts import render
from django.urls import include, path


@ensure_csrf_cookie
def home(request):
    return render(request, "home.html")


@login_required
def admin_support(request):
    if not (request.user.is_staff or getattr(request.user, "role", "") in {"admin", "support"}):
        raise PermissionDenied("You do not have permission to access the admin support panel.")
    return render(request, "admin_support.html")


urlpatterns = [
    path("", home, name="home"),
    path("admin-support/", admin_support, name="admin-support"),
    path("admin/", admin.site.urls),
    path("api/users/", include("apps.users.urls")),
    path("api/chat/", include("apps.chat.urls")),
    path("api/recommendations/", include("apps.recommendations.urls")),
    path("api/admin-panel/", include("apps.admin_panel.urls")),
    path("api/ai/", include("apps.ai_engine.urls")),
]

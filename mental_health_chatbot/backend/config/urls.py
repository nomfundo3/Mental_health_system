from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.views.decorators.csrf import ensure_csrf_cookie
from django.shortcuts import render
from django.urls import include, path
from django.views.generic import RedirectView

from apps.admin_panel.views import audit_logs_page


@ensure_csrf_cookie
def home(request):
    return render(request, "home.html")


@login_required
def admin_support(request):
    if not request.user.is_superuser:
        raise PermissionDenied("You do not have permission to access the superuser dashboard.")
    return render(request, "admin_panel/dashboard.html", {"active_page": "dashboard"})


urlpatterns = [
    path("", home, name="home"),
    path("admin-support/", admin_support, name="admin-support"),
    path("admin-support/audit/", audit_logs_page, name="admin-support-audit"),
    path("admin/", RedirectView.as_view(url="/admin-support/", permanent=False)),
    path("api/users/", include("apps.users.urls")),
    path("api/chat/", include("apps.chat.urls")),
    path("api/recommendations/", include("apps.recommendations.urls")),
    path("api/admin-panel/", include("apps.admin_panel.urls")),
    path("api/ai/", include("apps.ai_engine.urls")),
]

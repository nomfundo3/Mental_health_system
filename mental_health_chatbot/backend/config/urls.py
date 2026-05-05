from django.contrib import admin
from django.shortcuts import render
from django.urls import include, path


def home(request):
    return render(request, "home.html")


urlpatterns = [
    path("", home, name="home"),
    path("admin/", admin.site.urls),
    path("api/users/", include("apps.users.urls")),
    path("api/chat/", include("apps.chat.urls")),
    path("api/recommendations/", include("apps.recommendations.urls")),
    path("api/admin-panel/", include("apps.admin_panel.urls")),
    path("api/ai/", include("apps.ai_engine.urls")),
]

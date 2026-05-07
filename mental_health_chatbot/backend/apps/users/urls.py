from django.urls import path

from .views import CurrentUserView, UserLoginView, UserLogoutView, UserRegistrationView


urlpatterns = [
    path("me/", CurrentUserView.as_view(), name="user-me"),
    path("register/", UserRegistrationView.as_view(), name="user-register"),
    path("login/", UserLoginView.as_view(), name="user-login"),
    path("logout/", UserLogoutView.as_view(), name="user-logout"),
]

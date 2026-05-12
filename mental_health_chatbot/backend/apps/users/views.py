from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.middleware.csrf import get_token
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User
from .serializers import UserLoginSerializer, UserRegistrationSerializer


class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response(
            {
                "message": "Registration successful.",
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "display_name": user.display_name,
                    "role": user.role,
                    "preferred_language": user.preferred_language,
                },
            },
            status=status.HTTP_201_CREATED,
        )


class UserLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        identifier = serializer.validated_data["identifier"].strip()
        password = serializer.validated_data["password"]
        lookup_user = User.objects.filter(username__iexact=identifier).first()
        if lookup_user is None:
            lookup_user = User.objects.filter(email__iexact=identifier).first()

        username = lookup_user.username if lookup_user else identifier
        user = authenticate(request, username=username, password=password)

        if user is None:
            return Response(
                {"detail": "Invalid username or password."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not user.is_active:
            return Response(
                {"detail": "This account is inactive."},
                status=status.HTTP_403_FORBIDDEN,
            )

        login(request, user)
        return Response(
            {
                "message": "Login successful.",
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "display_name": user.display_name,
                    "role": user.role,
                    "preferred_language": user.preferred_language,
                },
            },
            status=status.HTTP_200_OK,
        )


class CurrentUserView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        get_token(request)
        guest_limit = getattr(settings, "GUEST_CHAT_TOKEN_LIMIT", 2400)
        guest_tokens_used = int(request.session.get("guest_chat_tokens_used", 0) or 0)
        guest_chat = {
            "token_limit": guest_limit,
            "tokens_used": guest_tokens_used,
            "tokens_remaining": max(guest_limit - guest_tokens_used, 0),
        }
        if not request.user.is_authenticated:
            return Response(
                {"authenticated": False, "user": None, "guest_chat": guest_chat},
                status=status.HTTP_200_OK,
            )

        user = request.user
        return Response(
            {
                "authenticated": True,
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "display_name": user.display_name,
                    "role": user.role,
                    "preferred_language": user.preferred_language,
                },
                "guest_chat": guest_chat,
            },
            status=status.HTTP_200_OK,
        )


class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        logout(request)
        return Response({"message": "Logout successful."}, status=status.HTTP_200_OK)

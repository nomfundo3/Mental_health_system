from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

from apps.chat.models import ChatMessage, ChatSession

User = get_user_model()


class AdminPanelTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_user(
            username="supportdemo",
            email="support@example.com",
            password="StrongPass123!",
            role="admin",
            is_staff=True,
            consent_accepted=True,
        )
        self.student_user = User.objects.create_user(
            username="student1",
            email="student1@example.com",
            password="StrongPass123!",
            role="student",
            consent_accepted=True,
        )
        session = ChatSession.objects.create(user=self.student_user)
        ChatMessage.objects.create(
            session=session,
            role="user",
            content="I want to kill myself",
            risk_level="high",
            sentiment="negative",
            flagged=True,
            detected_categories=["crisis"],
        )

    def test_admin_dashboard_requires_authorized_user(self):
        unauthorized = self.client.get("/api/admin-panel/dashboard/")
        self.assertEqual(unauthorized.status_code, 403)

        self.client.force_authenticate(user=self.student_user)
        forbidden = self.client.get("/api/admin-panel/dashboard/")
        self.assertEqual(forbidden.status_code, 403)

        self.client.force_authenticate(user=self.admin_user)
        allowed = self.client.get("/api/admin-panel/dashboard/")
        self.assertEqual(allowed.status_code, 200)
        self.assertEqual(allowed.json()["totals"]["flagged_messages"], 1)

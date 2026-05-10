from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient
from unittest.mock import patch

from apps.chat.models import ChatMessage, ChatSession, MoodCheckIn
from apps.recommendations.models import ResourceRecommendation

User = get_user_model()


class ChatWorkflowTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="student1",
            email="student1@example.com",
            password="StrongPass123!",
            consent_accepted=True,
        )
        ResourceRecommendation.objects.create(
            title="Stress Reset",
            description="A short grounding routine for exam stress.",
            category="stress",
            priority=5,
        )
        ResourceRecommendation.objects.create(
            title="Crisis Support",
            description="Seek urgent support immediately.",
            category="crisis",
            priority=10,
            is_emergency=True,
        )
        self.client.force_authenticate(user=self.user)

    def test_chat_message_creates_session_and_assessment(self):
        response = self.client.post(
            "/api/chat/message/",
            {"message": "I feel stressed about exams."},
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["assessment"]["risk_level"], "medium")
        self.assertEqual(ChatSession.objects.count(), 1)
        self.assertEqual(ChatMessage.objects.count(), 2)
        self.assertEqual(payload["session"]["messages"][-1]["role"], "assistant")

    def test_high_risk_message_is_flagged(self):
        response = self.client.post(
            "/api/chat/message/",
            {"message": "I want to kill myself."},
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["assessment"]["risk_level"], "high")
        self.assertTrue(payload["assessment"]["flagged"])
        self.assertEqual(payload["session"]["status"], "escalated")

        admin_user = User.objects.create_user(
            username="supportdemo",
            email="support@example.com",
            password="StrongPass123!",
            role="admin",
            is_staff=True,
            consent_accepted=True,
        )
        self.client.force_authenticate(user=admin_user)
        flagged_response = self.client.get("/api/admin-panel/flagged-messages/")
        self.assertEqual(flagged_response.status_code, 200)
        self.assertEqual(len(flagged_response.json()["flagged_messages"]), 1)

    def test_mood_checkin_can_attach_user_and_session(self):
        session = ChatSession.objects.create(user=self.user)
        response = self.client.post(
            "/api/chat/mood-checkins/",
            {
                "session_id": session.id,
                "mood": "anxious",
                "notes": "Presentation week is intense.",
                "stress_level": 4,
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        check_in = MoodCheckIn.objects.get()
        self.assertEqual(check_in.user, self.user)
        self.assertEqual(check_in.session, session)

    def test_sessions_endpoint_returns_only_authenticated_users_sessions(self):
        ChatSession.objects.create(user=self.user, title="Student Session")
        other_user = User.objects.create_user(
            username="student2",
            email="student2@example.com",
            password="StrongPass123!",
            consent_accepted=True,
        )
        ChatSession.objects.create(user=other_user, title="Other Session")

        response = self.client.get("/api/chat/sessions/")

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(len(payload), 1)
        self.assertEqual(payload[0]["title"], "Student Session")

    def test_chat_requires_authentication(self):
        self.client.force_authenticate(user=None)
        response = self.client.post(
            "/api/chat/message/",
            {"message": "I feel stressed about exams."},
            format="json",
        )
        self.assertEqual(response.status_code, 403)

    def test_cannot_post_into_another_users_session(self):
        other_user = User.objects.create_user(
            username="student2",
            email="student2@example.com",
            password="StrongPass123!",
            consent_accepted=True,
        )
        session = ChatSession.objects.create(user=other_user)

        response = self.client.post(
            "/api/chat/message/",
            {"session_id": session.id, "message": "This should be blocked."},
            format="json",
        )

        self.assertEqual(response.status_code, 403)

    @patch("services.response_service.generate_chat_response")
    @patch("services.response_service.is_llm_enabled", return_value=True)
    def test_llm_response_is_used_when_available(self, _, mock_generate_chat_response):
        mock_generate_chat_response.return_value = "Let's take one small step together."

        response = self.client.post(
            "/api/chat/message/",
            {"message": "I'm feeling low today."},
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["response_source"], "ai_service")
        self.assertEqual(payload["session"]["messages"][-1]["source"], "ai_service")

    @patch("services.response_service.generate_chat_response", side_effect=RuntimeError("provider error"))
    @patch("services.response_service.is_llm_enabled", return_value=True)
    def test_llm_failure_falls_back_safely(self, _, __):
        response = self.client.post(
            "/api/chat/message/",
            {"message": "I'm feeling low today."},
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["response_source"], "fallback")
        self.assertTrue(payload["session"]["messages"][-1]["fallback_used"])

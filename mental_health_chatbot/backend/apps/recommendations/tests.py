from django.test import TestCase
from rest_framework.test import APIClient

from apps.users.models import User
from apps.recommendations.models import ResourceRecommendation


class RecommendationTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        ResourceRecommendation.objects.create(
            title="General Help",
            description="General support.",
            category="general",
            priority=1,
            is_active=True,
        )
        ResourceRecommendation.objects.create(
            title="Stress Help",
            description="Stress support.",
            category="stress",
            priority=3,
            is_active=True,
        )
        ResourceRecommendation.objects.create(
            title="Emergency Help",
            description="Urgent support.",
            category="crisis",
            priority=10,
            is_active=True,
            is_emergency=True,
        )
        ResourceRecommendation.objects.create(
            title="Inactive Help",
            description="Should stay hidden.",
            category="stress",
            priority=8,
            is_active=False,
        )
        ResourceRecommendation.objects.create(
            title="Support Only Help",
            description="Support workflow only.",
            category="general",
            priority=9,
            audience="support",
            is_active=True,
        )

    def test_resource_list_returns_only_active_resources_sorted_by_priority(self):
        response = self.client.get("/api/recommendations/")

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual([item["title"] for item in payload], ["Emergency Help", "Stress Help", "General Help"])

    def test_resource_list_can_filter_by_category(self):
        response = self.client.get("/api/recommendations/?category=stress")

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(len(payload), 1)
        self.assertEqual(payload[0]["title"], "Stress Help")

    def test_resource_list_hides_support_only_resources_from_students_and_guests(self):
        response = self.client.get("/api/recommendations/")

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        titles = [item["title"] for item in payload]
        self.assertNotIn("Support Only Help", titles)

    def test_resource_list_allows_support_resources_for_support_users(self):
        support_user = User.objects.create_user(
            username="supportdemo",
            email="support@example.com",
            password="StrongPass123!",
            role="support",
            consent_accepted=True,
        )
        self.client.force_authenticate(user=support_user)

        response = self.client.get("/api/recommendations/")

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        titles = [item["title"] for item in payload]
        self.assertIn("Support Only Help", titles)

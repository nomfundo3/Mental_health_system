from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

User = get_user_model()


class UserApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_register_user(self):
        response = self.client.post(
            "/api/users/register/",
            {
                "username": "student1",
                "email": "student1@example.com",
                "display_name": "Student One",
                "preferred_language": "en",
                "password": "StrongPass123!",
                "confirm_password": "StrongPass123!",
                "consent_accepted": True,
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertTrue(User.objects.filter(username="student1").exists())

    def test_register_user_requires_consent(self):
        response = self.client.post(
            "/api/users/register/",
            {
                "username": "student1",
                "email": "student1@example.com",
                "password": "StrongPass123!",
                "confirm_password": "StrongPass123!",
                "consent_accepted": False,
            },
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("consent_accepted", response.json())

    def test_login_with_email(self):
        User.objects.create_user(
            username="student1",
            email="student1@example.com",
            password="StrongPass123!",
            consent_accepted=True,
        )

        response = self.client.post(
            "/api/users/login/",
            {"identifier": "student1@example.com", "password": "StrongPass123!"},
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["user"]["username"], "student1")

    def test_login_with_username(self):
        User.objects.create_user(
            username="student1",
            email="student1@example.com",
            password="StrongPass123!",
            consent_accepted=True,
        )

        response = self.client.post(
            "/api/users/login/",
            {"identifier": "student1", "password": "StrongPass123!"},
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["user"]["email"], "student1@example.com")

    def test_current_user_and_logout(self):
        user = User.objects.create_user(
            username="student1",
            email="student1@example.com",
            password="StrongPass123!",
            consent_accepted=True,
        )
        self.client.force_authenticate(user=user)

        me_response = self.client.get("/api/users/me/")
        self.assertEqual(me_response.status_code, 200)
        self.assertTrue(me_response.json()["authenticated"])

        logout_response = self.client.post("/api/users/logout/", {}, format="json")
        self.assertEqual(logout_response.status_code, 200)

    def test_logout_requires_authentication(self):
        response = self.client.post("/api/users/logout/", {}, format="json")
        self.assertEqual(response.status_code, 403)

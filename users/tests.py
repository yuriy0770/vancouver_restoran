from django.test import TestCase, Client
from django.urls import reverse
from .models import CustomUser


class UserTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_user_creation(self):
        user = CustomUser.objects.create_user(
            email="user@example.com", password="testpass123", first_name="John"
        )
        self.assertEqual(user.email, "user@example.com")
        self.assertEqual(user.get_display_name(), "John")

    def test_user_registration_view(self):
        response = self.client.get(reverse("users:register"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Регистрация")

    def test_user_login_view(self):
        response = self.client.get(reverse("users:login"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Вход в систему")

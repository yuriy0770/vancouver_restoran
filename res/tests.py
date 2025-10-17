from django.test import TestCase, Client
from django.urls import reverse


class MainPagesTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_home_page(self):
        response = self.client.get(reverse("res:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Maple Leaf")

    def test_menu_page(self):
        response = self.client.get(reverse("res:menu"))
        self.assertEqual(response.status_code, 200)

    def test_about_page(self):
        response = self.client.get(reverse("res:about"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Канадский клен")

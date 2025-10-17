from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Table, Reservation
from django.utils import timezone

User = get_user_model()


class ReservationTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email="test@example.com", password="testpass123"
        )
        self.table = Table.objects.create(
            number=1, seats=4, description="Test table", is_active=True
        )

    def test_table_creation(self):
        table = Table.objects.get(number=1)
        self.assertEqual(table.seats, 4)
        self.assertTrue(table.is_active)

    def test_reservation_creation(self):
        reservation = Reservation.objects.create(
            user=self.user,
            customer_name="Test User",
            customer_email="test@example.com",
            customer_phone="+1234567890",
            table=self.table,
            reservation_date=timezone.now().date(),
            reservation_time=timezone.now().time(),
            guests_count=2,
        )
        self.assertEqual(reservation.customer_name, "Test User")
        self.assertEqual(reservation.status, "confirmed")

    def test_reservation_view_requires_login(self):
        response = self.client.get(reverse("reservations:reservation"))
        self.assertEqual(response.status_code, 302)  # редирект на логин

    def test_reservation_view_with_login(self):
        self.client.login(email="test@example.com", password="testpass123")
        response = self.client.get(reverse("reservations:reservation"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Бронирование")

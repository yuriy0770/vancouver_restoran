from django.core.management.base import BaseCommand
from django.utils import timezone
from reservations.models import Reservation


class Command(BaseCommand):
    help = "Удаляет старые завершенные бронирования"

    def handle(self, *args, **options):
        old_date = timezone.now().date()
        old_reservations = Reservation.objects.filter(reservation_date__lt=old_date)

        count = old_reservations.count()
        old_reservations.delete()

        self.stdout.write(self.style.SUCCESS(f"✅ Удалено {count} старых бронирований"))

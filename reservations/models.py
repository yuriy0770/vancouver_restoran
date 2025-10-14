from django.db import models
from django.core.mail import send_mail
from django.conf import settings


class Table(models.Model):
    number = models.IntegerField(unique=True, verbose_name="Номер стола")
    seats = models.IntegerField(verbose_name="Количество мест")
    description = models.TextField(blank=True, verbose_name="Описание")
    is_active = models.BooleanField(default=True, verbose_name="Активен")

    def __str__(self):
        return f"Стол #{self.number} ({self.seats} мест)"


class Reservation(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидание'),
        ('confirmed', 'Подтверждено'),
        ('cancelled', 'Отменено'),
    ]

    customer_name = models.CharField(max_length=100, verbose_name="Имя гостя")
    customer_email = models.EmailField(verbose_name="Email гостя")
    customer_phone = models.CharField(max_length=20, verbose_name="Телефон")
    table = models.ForeignKey(Table, on_delete=models.CASCADE, verbose_name="Стол")
    reservation_date = models.DateField(verbose_name="Дата бронирования")
    reservation_time = models.TimeField(verbose_name="Время бронирования")
    guests_count = models.IntegerField(verbose_name="Количество гостей")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    notes = models.TextField(blank=True, verbose_name="Дополнительные пожелания")

    def __str__(self):
        return f"Бронь #{self.id} - {self.customer_name} - {self.reservation_date}"

    def send_confirmation_email(self):
        """Отправка email подтверждения"""
        subject = f'Подтверждение бронирования в ресторане "Канадский клен"'
        message = f'''
        Уважаемый(ая) {self.customer_name},

        Ваше бронирование подтверждено!

        Детали бронирования:
        - Дата: {self.reservation_date}
        - Время: {self.reservation_time}
        - Стол: #{self.table.number}
        - Количество гостей: {self.guests_count}

        Ресторан "Канадский клен"
        Телефон: +7 (XXX) XXX-XX-XX
        Адрес: [ваш адрес]

        Спасибо, что выбрали нас!
        '''

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [self.customer_email],
            fail_silently=False,
        )
from django.db import models
from django.conf import settings
from django.core.mail import send_mail


class Table(models.Model):
    number = models.IntegerField(unique=True, verbose_name="Номер стола")
    seats = models.IntegerField(verbose_name="Количество мест")
    description = models.TextField(blank=True, verbose_name="Описание")
    is_active = models.BooleanField(default=True, verbose_name="Активен")

    def __str__(self):
        return f"Стол #{self.number} ({self.seats} мест)"


class Reservation(models.Model):
    STATUS_CHOICES = [
        ("pending", "Ожидание"),
        ("confirmed", "Подтверждено"),
        ("cancelled", "Отменено"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        null=True,
        blank=True,
    )
    customer_name = models.CharField(max_length=100, verbose_name="Имя гостя")
    customer_email = models.EmailField(verbose_name="Email гостя")
    customer_phone = models.CharField(max_length=20, verbose_name="Телефон")
    table = models.ForeignKey(
        Table, on_delete=models.CASCADE, verbose_name="Стол"
    )  # Теперь Table определен выше
    reservation_date = models.DateField(verbose_name="Дата бронирования")
    reservation_time = models.TimeField(verbose_name="Время бронирования")
    guests_count = models.IntegerField(verbose_name="Количество гостей")
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="confirmed"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    notes = models.TextField(blank=True, verbose_name="Дополнительные пожелания")

    def __str__(self):
        return f"Бронь #{self.id} - {self.customer_name} - {self.reservation_date}"

    def save(self, *args, **kwargs):
        if self.user and not self.customer_email:
            self.customer_email = self.user.email
        if self.user and not self.customer_name:
            self.customer_name = self.user.email.split("@")[0]
        super().save(*args, **kwargs)

    def send_confirmation_email(self):

        subject = 'Подтверждение бронирования в ресторане "Канадский клен"'

        message = f"""
    Уважаемый(ая) {self.customer_name},

    Ваше бронирование подтверждено!

    🎯 Детали бронирования:
    • Дата: {self.reservation_date}
    • Время: {self.reservation_time}
    • Стол: #{self.table.number} ({self.table.seats} мест)
    • Количество гостей: {self.guests_count}

    📍 Ресторан "Канадский клен"
    📞 Телефон: +7 (XXX) XXX-XX-XX
    

    💡 Пожалуйста, приходите за 10-15 минут до назначенного времени.

    Если у вас изменились планы, пожалуйста, сообщите нам по телефону.

    Спасибо, что выбрали нас!
    С нетерпением ждем вас!

    --
    С уважением,
    Команда ресторана "Канадский клен"
    """

        from django.core.mail import send_mail
        from django.conf import settings

        try:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [self.customer_email],
                fail_silently=False,
            )
            return True
        except Exception as e:
            print(f"Ошибка отправки email: {e}")
            return False

        from django.core.mail import send_mail
        from django.conf import settings

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [self.customer_email],
            fail_silently=False,
        )

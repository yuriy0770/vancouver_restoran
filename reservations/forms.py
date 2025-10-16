from django import forms
from django.core.exceptions import ValidationError
from .models import Reservation, Table
from django.utils import timezone


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = [
            "customer_name",
            "customer_email",
            "customer_phone",
            "table",
            "reservation_date",
            "reservation_time",
            "guests_count",
            "notes",
        ]
        widgets = {
            "reservation_date": forms.DateInput(
                attrs={
                    "type": "date",
                    "min": timezone.now().date().isoformat(),
                    "class": "form-control",
                    "id": "id_reservation_date",
                }
            ),
            "reservation_time": forms.TimeInput(
                attrs={
                    "type": "time",
                    "class": "form-control",
                    "id": "id_reservation_time",
                }
            ),
            "notes": forms.Textarea(attrs={"rows": 4, "class": "form-control"}),
            "customer_name": forms.TextInput(attrs={"class": "form-control"}),
            "customer_email": forms.EmailInput(attrs={"class": "form-control"}),
            "customer_phone": forms.TextInput(attrs={"class": "form-control"}),
            "guests_count": forms.NumberInput(
                attrs={"class": "form-control", "min": 1}
            ),
            "table": forms.Select(attrs={"class": "form-control", "id": "id_table"}),
        }
        labels = {
            "customer_name": "Ваше имя *",
            "customer_email": "Email *",
            "customer_phone": "Телефон *",
            "reservation_date": "Дата *",
            "reservation_time": "Время *",
            "guests_count": "Количество гостей *",
            "table": "Выберите стол *",
            "notes": "Дополнительные пожелания",
        }

    def clean(self):
        cleaned_data = super().clean()
        table = cleaned_data.get("table")
        reservation_date = cleaned_data.get("reservation_date")
        reservation_time = cleaned_data.get("reservation_time")

        if table and reservation_date and reservation_time:
            conflicting_booking = Reservation.objects.filter(
                table=table,
                reservation_date=reservation_date,
                reservation_time=reservation_time,
                status__in=["pending", "confirmed"],
            ).exists()

            if conflicting_booking:
                raise ValidationError(
                    f"❌ Стол #{table.number} только что был забронирован на {reservation_date} в {reservation_time}. "
                    f"Пожалуйста, выберите другое время или другой стол."
                )

        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        reservation_date = None
        reservation_time = None

        if self.data:
            reservation_date = self.data.get("reservation_date")
            reservation_time = self.data.get("reservation_time")
        elif self.initial:
            reservation_date = self.initial.get("reservation_date")
            reservation_time = self.initial.get("reservation_time")


        self.fields["table"].queryset = self.get_available_tables(
            reservation_date, reservation_time
        )


        self.fields["reservation_date"].widget.attrs["min"] = (
            timezone.now().date().isoformat()
        )

    def get_available_tables(self, reservation_date=None, reservation_time=None):

        available_tables = Table.objects.filter(is_active=True)

        if reservation_date and reservation_time:

            booked_tables = Reservation.objects.filter(
                reservation_date=reservation_date,
                reservation_time=reservation_time,
                status__in=["pending", "confirmed"],
            ).values_list("table_id", flat=True)


            available_tables = available_tables.exclude(id__in=booked_tables)

        return available_tables

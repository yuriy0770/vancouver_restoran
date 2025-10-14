from django import forms
from .models import Reservation, Table
from django.utils import timezone


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['customer_name', 'customer_email', 'customer_phone',
                  'table', 'reservation_date', 'reservation_time', 'guests_count', 'notes']  # Добавил 'table'
        widgets = {
            'reservation_date': forms.DateInput(attrs={
                'type': 'date',
                'min': timezone.now().date().isoformat(),
                'class': 'form-control'
            }),
            'reservation_time': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'form-control'
            }),
            'notes': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'customer_name': forms.TextInput(attrs={'class': 'form-control'}),
            'customer_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'customer_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'guests_count': forms.NumberInput(attrs={'class': 'form-control'}),
            'table': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'customer_name': 'Ваше имя *',
            'customer_email': 'Email *',
            'customer_phone': 'Телефон *',
            'reservation_date': 'Дата *',
            'reservation_time': 'Время *',
            'guests_count': 'Количество гостей *',
            'table': 'Выберите стол *',
            'notes': 'Дополнительные пожелания',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Фильтруем только активные столы
        self.fields['table'].queryset = Table.objects.filter(is_active=True)

        # Устанавливаем минимальную дату
        self.fields['reservation_date'].widget.attrs['min'] = timezone.now().date().isoformat()
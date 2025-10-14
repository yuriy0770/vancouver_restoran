from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Reservation, Table
from .forms import ReservationForm


def reservation_view(request):
    available_tables = Table.objects.filter(is_active=True)

    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.status = 'confirmed'
            reservation.save()

            # Пытаемся отправить email
            try:
                reservation.send_confirmation_email()
                messages.success(request, 'Бронирование успешно создано! На вашу почту отправлено подтверждение.')
            except Exception as e:
                print(f"Email error: {e}")  # Для дебага
                messages.success(request, 'Бронирование успешно создано!')

            return redirect('reservations:reservation_success')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = ReservationForm()

    return render(request, 'reservations/reservation.html', {
        'form': form,
        'available_tables': available_tables,
    })


def reservation_success(request):
    return render(request, 'reservations/success.html')
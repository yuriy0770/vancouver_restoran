from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Reservation, Table
from .forms import ReservationForm
from django.utils import timezone
from .telegram_bot import send_telegram_notification


@login_required
def reservation_view(request):
    if request.method == "POST":
        form = ReservationForm(request.POST)
        if form.is_valid():
            try:
                reservation = form.save(commit=False)
                reservation.user = request.user
                reservation.status = "confirmed"
                reservation.save()

                telegram_message = f"""
📞 <b>НОВОЕ БРОНИРОВАНИЕ</b>

👤 Имя: {reservation.customer_name}
📧 Email: {reservation.customer_email}
📞 Телефон: {reservation.customer_phone}
📅 Дата: {reservation.reservation_date}
⏰ Время: {reservation.reservation_time}
🍽 Стол: #{reservation.table.number} ({reservation.table.seats} мест)
👥 Гостей: {reservation.guests_count}
💬 Пожелания: {reservation.notes or 'нет'}
                """
                send_telegram_notification(telegram_message)

                return redirect(
                    "reservations:reservation_success", reservation_id=reservation.id
                )

            except Exception as e:
                messages.error(request, f"Ошибка при создании бронирования: {e}")
    else:
        initial_data = {
            "customer_email": request.user.email,
            "customer_name": request.user.get_display_name(),
        }
        form = ReservationForm(initial=initial_data)

    today = timezone.now().date()

    active_reservations = Reservation.objects.filter(
        reservation_date__gte=today, status__in=["pending", "confirmed"]
    )

    booked_table_ids = active_reservations.values_list("table_id", flat=True)
    all_tables = Table.objects.filter(is_active=True)
    available_tables = all_tables.exclude(id__in=booked_table_ids)
    booked_tables = all_tables.filter(id__in=booked_table_ids)

    return render(
        request,
        "reservations/reservation.html",
        {
            "form": form,
            "available_tables": available_tables,
            "booked_tables": booked_tables,
        },
    )


@login_required
def reservation_success(request, reservation_id):
    try:
        reservation = Reservation.objects.get(id=reservation_id, user=request.user)
        return render(
            request, "reservations/success.html", {"reservation": reservation}
        )
    except Reservation.DoesNotExist:
        messages.error(request, "Бронирование не найдено")
        return redirect("reservations:reservation")

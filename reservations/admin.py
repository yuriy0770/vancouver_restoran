from django.contrib import admin
from django.utils import timezone
from .models import Table, Reservation


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ["number", "seats", "is_active", "is_available_today"]
    list_filter = ["is_active"]
    search_fields = ["number"]
    list_editable = ["is_active"]
    actions = ["activate_tables", "deactivate_tables"]

    def is_available_today(self, obj):
        today = timezone.now().date()
        reservations_today = Reservation.objects.filter(
            table=obj,
            reservation_date=today,
            status__in=['pending', 'confirmed']
        )
        return not reservations_today.exists()

    is_available_today.boolean = True
    is_available_today.short_description = "Свободен сегодня"

    def activate_tables(self, request, queryset):
        queryset.update(is_active=True)

    activate_tables.short_description = "Активировать выбранные столы"

    def deactivate_tables(self, request, queryset):
        queryset.update(is_active=False)

    deactivate_tables.short_description = "Деактивировать выбранные столы"


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "customer_name",
        "customer_email",
        "table",
        "reservation_date",
        "reservation_time",
        "guests_count",
        "status",
        "created_at"
    ]
    list_filter = ["status", "reservation_date", "table"]
    search_fields = ["customer_name", "customer_email", "customer_phone"]
    list_editable = ["status"]
    date_hierarchy = "reservation_date"
    actions = ["confirm_reservations", "cancel_reservations"]

    def confirm_reservations(self, request, queryset):
        queryset.update(status='confirmed')

    confirm_reservations.short_description = "Подтвердить выбранные бронирования"

    def cancel_reservations(self, request, queryset):
        queryset.update(status='cancelled')

    cancel_reservations.short_description = "Отменить выбранные бронирования"

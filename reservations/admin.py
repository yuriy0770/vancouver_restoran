from django.contrib import admin
from .models import Table, Reservation


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ["number", "seats", "is_active"]
    list_filter = ["is_active"]
    search_fields = ["number"]


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "customer_name",
        "customer_email",
        "table",
        "reservation_date",
        "status",
    ]
    list_filter = ["status", "reservation_date"]
    search_fields = ["customer_name", "customer_email"]

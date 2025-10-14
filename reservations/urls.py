from django.urls import path
from . import views

app_name = 'reservations'

urlpatterns = [
    path('', views.reservation_view, name='reservation'),
    path('success/', views.reservation_success, name='reservation_success'),
]

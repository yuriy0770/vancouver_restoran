from django.urls import path
from . import views

app_name = "res"

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("menu/", views.MenuView.as_view(), name="menu"),
    path(
        "category/<int:pk>/", views.CategoryDetailView.as_view(), name="category_detail"
    ),
    path("dish/<int:pk>/", views.DishDetailView.as_view(), name="dish_detail"),
    path("about/", views.about, name="about"),
    path("reviews/", views.reviews_list, name="reviews_list"),
    path("reviews/new/", views.review_create, name="review_create"),
]

from django.contrib import admin
from .models import Category, Dishes, Review


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'title', 'image']
    list_display_links = ['name', 'title', 'image']
    search_fields = ['name']
    list_filter = ['name', 'title']

@admin.register(Dishes)
class DishesAdmin(admin.ModelAdmin):
    list_display = ['name_dish', 'price', 'body', 'image_dish', 'cat']
    list_display_links = ['name_dish']
    search_fields = ['name_dish']
    list_filter = ['name_dish', 'price']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('author', 'dish', 'rating', 'is_published', 'created_at')
    list_filter = ('is_published','created_at')
    search_fields = ('author','email','text')
    actions = ['publish reviews']

    def publish_reviews(self, request, queryset):
        updated = queryset.update(is_published=True)
        self.message_user(request, f'{updated} отзыв(ов) опубликовано')
    publish_reviews.short_description = "Опубликовать выбранные отзывы"

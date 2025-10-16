from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=30, blank=True)
    title = models.CharField(max_length=50, blank=True)
    image = models.ImageField(upload_to="category/photo", blank=True, null=True)

    def __str__(self):
        return self.name or ""

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["name"]
        indexes = [
            models.Index(fields=["name"]),
        ]


class Dishes(models.Model):
    name_dish = models.CharField(max_length=100)
    price = models.IntegerField()
    short_description = models.CharField(max_length=255, blank=True)  # рекомендовано
    body = models.TextField(blank=True)
    ingredients = models.TextField(blank=True)  # рекомендовано
    is_available = models.BooleanField(default=True)  # рекомендовано
    image_dish = models.ImageField(upload_to="dishes/photo", blank=True, null=True)
    cat = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="dishes")

    def __str__(self):
        return self.name_dish

    class Meta:
        verbose_name = "Блюдо"
        verbose_name_plural = "Блюда"
        ordering = ["name_dish"]
        indexes = [
            models.Index(fields=["name_dish"]),
        ]


class Review(models.Model):
    author = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    dish = models.ForeignKey(
        Dishes, null=True, blank=True, on_delete=models.CASCADE, related_name="reviews"
    )
    text = models.TextField()
    rating = models.PositiveSmallIntegerField(null=True, blank=True)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        target = self.dish.name_dish if self.dish else "Общий отзыв"
        return f"{self.author} — {target} ({self.created_at.date()})"

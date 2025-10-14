from django.views.generic import TemplateView, ListView, DetailView
from .models import Category, Dishes
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Review
from .forms import ReviewForm

class IndexView(TemplateView):
    template_name = 'res/index.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        # для главной: крупные картинки (можно хранить в static) и избранные блюда
        ctx['featured dishes'] = Dishes.objects.filter(is_available=True)[:6]
        ctx['about text'] = (
            "Welcome to Maple Leaf — authentic Canadian cuisine. "
            "Try our poutine, butter tarts and seasonal specialties."
        )
        # можно показать несколько категорий как миниатюры (опционально) или не показывать вовсе
        return ctx

class MenuView(ListView):
    model = Category
    template_name = 'res/menu.html'
    context_object_name = 'categories'

class CategoryDetailView(DetailView):
    model = Category
    template_name = 'res/category_detail.html'
    context_object_name = 'category'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['dishes'] = self.object.dishes.filter(is_available=True)
        return ctx

class DishDetailView(DetailView):
    model = Dishes
    template_name = 'res/dish_detail.html'
    context_object_name = 'dish'

def about(request):
    about_text = (
        "Наш ресторан сочетает классические рецепты и современные техники. "
        "Мы используем только свежие продукты от проверенных поставщиков."
    )
    images = [
        'images/about1.jpg',
        'images/about2.jpg',
        'images/about3.jpg',
        'images/about4.jpg',
        'images/about5.jpg',
        'images/about6.jpg',
    ]
    return render(request, 'res/about.html', {
        'about_text': about_text,
        'about_images': images,
        'page_title': 'О нас',
    })




def reviews_list(request):
    reviews = Review.objects.filter(is_published=True).select_related('dish')
    form = ReviewForm(initial={'dish': None})
    return render(request, 'res/reviews_list.html', {'reviews': reviews, 'form': form})

def review_create(request):
    if request.method != 'POST':
        return redirect('res:reviews_list')
    form = ReviewForm(request.POST)
    if form.is_valid():
        review = form.save(commit=False)
        review.is_published = False
        review.save()
        messages.success(request, 'Спасибо! Ваш отзыв отправлен на модерацию.')
        return redirect('res:reviews_list')
    reviews = Review.objects.filter(is_published=True).select_related('dish')
    return render(request, 'res/reviews_list.html', {'reviews': reviews, 'form': form})




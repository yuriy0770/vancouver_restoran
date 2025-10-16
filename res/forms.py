from django import forms
from .models import Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ("author", "email", "dish", "rating", "text")
        widgets = {
            "author": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Имя"}
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "email@example.com"}
            ),
            "dish": forms.HiddenInput(),
            "rating": forms.Select(
                attrs={"class": "form-select"},
                choices=[("", "—")] + [(i, str(i)) for i in range(1, 6)],
            ),
            "text": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Расскажите о впечатлении...",
                }
            ),
        }

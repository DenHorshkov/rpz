from django import forms

from .models import Review


class ReviewForm(forms.ModelForm):
    rating = forms.IntegerField(
        label="Оцінка (1–5)",
        min_value=1,
        max_value=5,
        widget=forms.NumberInput(attrs={"min": 1, "max": 5}),
    )

    class Meta:
        model = Review
        fields = ("rating", "text")
        widgets = {"text": forms.Textarea(attrs={"rows": 4})}

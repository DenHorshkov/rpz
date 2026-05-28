from django import forms

from .models import Product, ProductImage


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ("category", "title", "description", "price", "stock", "is_active")
        widgets = {
            "description": forms.Textarea(attrs={"rows": 5}),
        }


class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ("image", "alt_text")

    def clean_image(self):
        image = self.cleaned_data.get("image")
        if image and image.size > 5 * 1024 * 1024:
            raise forms.ValidationError("Розмір файлу не повинен перевищувати 5 МБ.")
        return image

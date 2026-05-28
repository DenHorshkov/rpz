from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import MasterProfile, User


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(label="Email", required=True)
    first_name = forms.CharField(label="Ім'я", required=False, max_length=150)
    last_name = forms.CharField(label="Прізвище", required=False, max_length=150)

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "password1", "password2")

    def clean_email(self) -> str:
        email = self.cleaned_data["email"]
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Користувач з таким email вже існує.")
        return email


class MasterProfileForm(forms.ModelForm):
    class Meta:
        model = MasterProfile
        fields = ("display_name", "bio", "avatar", "city", "contact_phone")
        widgets = {
            "bio": forms.Textarea(attrs={"rows": 4}),
        }

    def clean_avatar(self):
        avatar = self.cleaned_data.get("avatar")
        if avatar and avatar.size > 3 * 1024 * 1024:
            raise forms.ValidationError("Розмір файлу не повинен перевищувати 3 МБ.")
        return avatar

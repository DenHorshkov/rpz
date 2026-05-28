from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class User(AbstractUser):
    email = models.EmailField("Email", unique=True)

    class Meta:
        verbose_name = "Користувач"
        verbose_name_plural = "Користувачі"

    @property
    def is_seller(self) -> bool:
        return hasattr(self, "master_profile")

    def __str__(self) -> str:
        return self.get_full_name() or self.username


class MasterProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="master_profile",
        verbose_name="Користувач",
    )
    display_name = models.CharField("Назва майстерні", max_length=120)
    bio = models.TextField("Про себе", blank=True)
    avatar = models.ImageField("Аватар", upload_to="avatars/", blank=True, null=True)
    city = models.CharField("Місто", max_length=80, blank=True)
    contact_phone = models.CharField("Контактний телефон", max_length=32, blank=True)
    created_at = models.DateTimeField("Створено", auto_now_add=True)

    class Meta:
        verbose_name = "Профіль майстра"
        verbose_name_plural = "Профілі майстрів"
        ordering = ["display_name"]

    def __str__(self) -> str:
        return self.display_name

    def get_absolute_url(self) -> str:
        return reverse("accounts:master_detail", args=[self.pk])

    @property
    def average_rating(self) -> float | None:
        from apps.reviews.models import Review

        agg = Review.objects.filter(seller=self).aggregate(models.Avg("rating"))
        return agg["rating__avg"]

    @property
    def review_count(self) -> int:
        from apps.reviews.models import Review

        return Review.objects.filter(seller=self).count()

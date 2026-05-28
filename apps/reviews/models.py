from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from apps.accounts.models import MasterProfile
from apps.orders.models import Order


class Review(models.Model):
    seller = models.ForeignKey(
        MasterProfile,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Продавець",
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="written_reviews",
        verbose_name="Автор",
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="reviews",
        verbose_name="Замовлення",
    )
    rating = models.PositiveSmallIntegerField(
        "Оцінка",
        validators=[MinValueValidator(1), MaxValueValidator(5)],
    )
    text = models.TextField("Текст відгуку")
    created_at = models.DateTimeField("Створено", auto_now_add=True)

    class Meta:
        verbose_name = "Відгук"
        verbose_name_plural = "Відгуки"
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=("seller", "author", "order"),
                name="unique_review_per_order",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.author} → {self.seller} ({self.rating}/5)"

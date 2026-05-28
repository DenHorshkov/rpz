from decimal import Decimal

from django.conf import settings
from django.db import models
from django.urls import reverse

from apps.catalog.models import Product


class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Очікує оплати"
        PAID = "paid", "Оплачено"
        SHIPPED = "shipped", "Відправлено"
        DELIVERED = "delivered", "Доставлено"
        CANCELLED = "cancelled", "Скасовано"

    buyer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="orders",
        verbose_name="Покупець",
    )
    status = models.CharField("Статус", max_length=16, choices=Status.choices, default=Status.PENDING)
    full_name = models.CharField("ПІБ", max_length=120)
    phone = models.CharField("Телефон", max_length=32)
    address = models.CharField("Адреса доставки", max_length=255)
    comment = models.TextField("Коментар", blank=True)
    total = models.DecimalField("Сума", max_digits=12, decimal_places=2, default=Decimal("0"))
    created_at = models.DateTimeField("Створено", auto_now_add=True)
    paid_at = models.DateTimeField("Оплачено", blank=True, null=True)

    class Meta:
        verbose_name = "Замовлення"
        verbose_name_plural = "Замовлення"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"Замовлення #{self.pk}"

    def get_absolute_url(self) -> str:
        return reverse("orders:detail", args=[self.pk])

    def recalc_total(self) -> None:
        self.total = sum((item.subtotal for item in self.items.all()), Decimal("0"))
        self.save(update_fields=["total"])


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name="order_items")
    title = models.CharField("Назва на момент замовлення", max_length=160)
    price = models.DecimalField("Ціна на момент замовлення", max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField("Кількість")

    class Meta:
        verbose_name = "Позиція замовлення"
        verbose_name_plural = "Позиції замовлення"

    @property
    def subtotal(self) -> Decimal:
        return self.price * self.quantity

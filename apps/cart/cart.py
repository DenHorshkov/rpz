"""Сесійний кошик: тонкий wrapper над request.session['cart'] = {product_id: qty}."""
from decimal import Decimal
from typing import Iterator

from django.http import HttpRequest

from apps.catalog.models import Product

SESSION_KEY = "cart"


class Cart:
    def __init__(self, request: HttpRequest) -> None:
        self.session = request.session
        self.cart: dict[str, int] = self.session.setdefault(SESSION_KEY, {})

    def save(self) -> None:
        self.session[SESSION_KEY] = self.cart
        self.session.modified = True

    def add(self, product: Product, quantity: int = 1, replace: bool = False) -> None:
        pid = str(product.pk)
        current = 0 if replace else self.cart.get(pid, 0)
        new_qty = max(1, min(current + quantity, product.stock))
        self.cart[pid] = new_qty
        self.save()

    def remove(self, product: Product) -> None:
        self.cart.pop(str(product.pk), None)
        self.save()

    def clear(self) -> None:
        self.session[SESSION_KEY] = {}
        self.cart = self.session[SESSION_KEY]
        self.session.modified = True

    def items(self) -> Iterator[dict]:
        if not self.cart:
            return iter(())
        product_ids = [int(pid) for pid in self.cart.keys()]
        products = Product.objects.filter(pk__in=product_ids).select_related("owner")
        for product in products:
            qty = self.cart[str(product.pk)]
            yield {
                "product": product,
                "quantity": qty,
                "subtotal": product.price * qty,
            }

    @property
    def count(self) -> int:
        return sum(self.cart.values())

    @property
    def total(self) -> Decimal:
        total = Decimal("0")
        for item in self.items():
            total += item["subtotal"]
        return total

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from apps.catalog.models import Product

from .cart import Cart


@require_POST
def add(request, product_id: int):
    product = get_object_or_404(Product, pk=product_id, is_active=True)
    quantity = int(request.POST.get("quantity", 1))
    cart = Cart(request)
    cart.add(product, quantity=quantity)
    messages.success(request, f"«{product.title}» додано в кошик.")
    return redirect("cart:detail")


@require_POST
def update(request, product_id: int):
    product = get_object_or_404(Product, pk=product_id)
    quantity = int(request.POST.get("quantity", 1))
    cart = Cart(request)
    cart.add(product, quantity=quantity, replace=True)
    return redirect("cart:detail")


@require_POST
def remove(request, product_id: int):
    product = get_object_or_404(Product, pk=product_id)
    Cart(request).remove(product)
    messages.info(request, f"«{product.title}» видалено з кошика.")
    return redirect("cart:detail")


def detail(request):
    cart = Cart(request)
    return render(request, "cart/detail.html", {"cart": cart, "items": list(cart.items())})


@require_POST
def clear(request):
    Cart(request).clear()
    return redirect("cart:detail")

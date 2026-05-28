from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from apps.cart.cart import Cart

from .forms import CheckoutForm
from .models import Order, OrderItem


@login_required
def checkout(request):
    cart = Cart(request)
    items = list(cart.items())
    if not items:
        messages.warning(request, "Кошик порожній.")
        return redirect("catalog:product_list")

    initial = {
        "full_name": request.user.get_full_name() or request.user.username,
    }

    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                order: Order = form.save(commit=False)
                order.buyer = request.user
                order.save()
                for item in items:
                    OrderItem.objects.create(
                        order=order,
                        product=item["product"],
                        title=item["product"].title,
                        price=item["product"].price,
                        quantity=item["quantity"],
                    )
                order.recalc_total()
            return redirect("orders:detail", pk=order.pk)
    else:
        form = CheckoutForm(initial=initial)

    return render(request, "orders/checkout.html", {"form": form, "items": items, "total": cart.total})


@login_required
def detail(request, pk: int):
    order = get_object_or_404(Order.objects.prefetch_related("items"), pk=pk, buyer=request.user)
    return render(request, "orders/detail.html", {"order": order})


@login_required
@require_POST
def pay(request, pk: int):
    order = get_object_or_404(Order, pk=pk, buyer=request.user)
    if order.status != Order.Status.PENDING:
        messages.info(request, "Замовлення вже опрацьоване.")
        return redirect(order.get_absolute_url())
    order.status = Order.Status.PAID
    order.paid_at = timezone.now()
    order.save(update_fields=["status", "paid_at"])
    Cart(request).clear()
    messages.success(request, f"✔ Замовлення #{order.pk} оплачено. Дякуємо за покупку!")
    return redirect(order.get_absolute_url())


@login_required
def my_orders(request):
    orders = Order.objects.filter(buyer=request.user).prefetch_related("items")
    return render(request, "orders/my_orders.html", {"orders": orders})

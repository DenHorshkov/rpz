from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, redirect, render

from apps.accounts.models import MasterProfile
from apps.orders.models import Order

from .forms import ReviewForm


@login_required
def create(request, master_id: int):
    seller = get_object_or_404(MasterProfile, pk=master_id)

    order_id = request.GET.get("order") or request.POST.get("order")
    order = None
    if order_id:
        order = Order.objects.filter(
            pk=order_id,
            buyer=request.user,
            status=Order.Status.PAID,
            items__product__owner=seller,
        ).distinct().first()

    eligible_order_exists = Order.objects.filter(
        buyer=request.user,
        status=Order.Status.PAID,
        items__product__owner=seller,
    ).exists()

    if not eligible_order_exists:
        messages.error(request, "Залишати відгуки можуть лише покупці з оплаченим замовленням у цього майстра.")
        return redirect(seller.get_absolute_url())

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.seller = seller
            review.author = request.user
            review.order = order
            try:
                review.save()
            except IntegrityError:
                messages.warning(request, "Ви вже залишали відгук для цього замовлення.")
                return redirect(seller.get_absolute_url())
            messages.success(request, "Дякуємо за відгук!")
            return redirect(seller.get_absolute_url())
    else:
        form = ReviewForm()
    return render(request, "reviews/create.html", {"form": form, "seller": seller, "order": order})

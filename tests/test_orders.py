import pytest
from django.urls import reverse

from apps.orders.models import Order


@pytest.mark.django_db
def test_checkout_creates_order_and_pay_marks_paid(client, buyer, product):
    client.force_login(buyer)
    client.post(reverse("cart:add", args=[product.pk]), {"quantity": 2})

    response = client.post(
        reverse("orders:checkout"),
        {
            "full_name": "Тест Тестович",
            "phone": "+380501112233",
            "address": "Київ, вул. Тестова, 1",
            "comment": "",
        },
    )
    assert response.status_code == 302
    order = Order.objects.get(buyer=buyer)
    assert order.status == Order.Status.PENDING
    assert order.items.count() == 1
    assert order.total == product.price * 2

    response = client.post(reverse("orders:pay", args=[order.pk]))
    assert response.status_code == 302
    order.refresh_from_db()
    assert order.status == Order.Status.PAID
    assert order.paid_at is not None
    assert client.session.get("cart", {}) == {}


@pytest.mark.django_db
def test_pay_other_users_order_is_forbidden(client, buyer, seller_user, product):
    client.force_login(buyer)
    client.post(reverse("cart:add", args=[product.pk]), {"quantity": 1})
    client.post(
        reverse("orders:checkout"),
        {"full_name": "X", "phone": "+380", "address": "Y", "comment": ""},
    )
    order = Order.objects.get(buyer=buyer)

    client.force_login(seller_user)
    response = client.post(reverse("orders:pay", args=[order.pk]))
    assert response.status_code == 404

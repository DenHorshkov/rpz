import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_add_to_cart_increments_count(client, product):
    response = client.post(reverse("cart:add", args=[product.pk]), {"quantity": 2})
    assert response.status_code == 302
    session = client.session
    assert session["cart"][str(product.pk)] == 2


@pytest.mark.django_db
def test_remove_from_cart(client, product):
    client.post(reverse("cart:add", args=[product.pk]), {"quantity": 1})
    client.post(reverse("cart:remove", args=[product.pk]))
    session = client.session
    assert str(product.pk) not in session.get("cart", {})


@pytest.mark.django_db
def test_cart_caps_quantity_to_stock(client, product):
    response = client.post(reverse("cart:add", args=[product.pk]), {"quantity": 999})
    assert response.status_code == 302
    assert client.session["cart"][str(product.pk)] == product.stock

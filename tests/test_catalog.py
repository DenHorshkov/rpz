import pytest
from django.urls import reverse

from apps.catalog.models import Product


@pytest.mark.django_db
def test_product_list_shows_active_products(client, product):
    response = client.get(reverse("catalog:product_list"))
    assert response.status_code == 200
    assert product.title.encode() in response.content


@pytest.mark.django_db
def test_only_owner_can_delete_product(client, product, buyer):
    client.force_login(buyer)
    response = client.post(reverse("catalog:product_delete", args=[product.slug]))
    assert response.status_code == 302
    assert Product.objects.filter(pk=product.pk).exists()


@pytest.mark.django_db
def test_owner_can_edit_product(client, product, seller_user):
    client.force_login(seller_user)
    response = client.post(
        reverse("catalog:product_edit", args=[product.slug]),
        {
            "category": product.category_id,
            "title": "Оновлена назва",
            "description": product.description,
            "price": "400.00",
            "stock": 3,
            "is_active": "on",
        },
    )
    assert response.status_code in (302, 200)
    product.refresh_from_db()
    assert product.title == "Оновлена назва"

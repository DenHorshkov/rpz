import pytest
from django.urls import reverse

from apps.orders.models import Order, OrderItem
from apps.reviews.models import Review


@pytest.fixture
def paid_order(buyer, product):
    order = Order.objects.create(
        buyer=buyer,
        status=Order.Status.PAID,
        full_name="Buyer",
        phone="+380",
        address="X",
        total=product.price,
    )
    OrderItem.objects.create(
        order=order, product=product, title=product.title, price=product.price, quantity=1
    )
    return order


@pytest.mark.django_db
def test_review_blocked_without_paid_order(client, buyer, seller_profile):
    client.force_login(buyer)
    response = client.post(
        reverse("reviews:create", args=[seller_profile.pk]),
        {"rating": 5, "text": "Чудово"},
    )
    assert response.status_code == 302
    assert Review.objects.count() == 0


@pytest.mark.django_db
def test_review_created_after_paid_order(client, buyer, seller_profile, paid_order):
    client.force_login(buyer)
    response = client.post(
        reverse("reviews:create", args=[seller_profile.pk]) + f"?order={paid_order.pk}",
        {"rating": 5, "text": "Дуже сподобалось", "order": paid_order.pk},
    )
    assert response.status_code == 302
    review = Review.objects.get()
    assert review.rating == 5
    assert review.seller == seller_profile


@pytest.mark.django_db
def test_average_rating_aggregated(client, buyer, seller_profile, paid_order, seller_user):
    Review.objects.create(seller=seller_profile, author=buyer, rating=4, text="ok")
    other = type(buyer).objects.create_user(username="b2", email="b2@e.com", password="x")
    Review.objects.create(seller=seller_profile, author=other, rating=2, text="meh")
    assert seller_profile.average_rating == 3.0
    assert seller_profile.review_count == 2

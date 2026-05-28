import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


@pytest.mark.django_db
def test_registration_creates_user_and_logs_in(client):
    response = client.post(
        reverse("accounts:register"),
        {
            "username": "newbie",
            "email": "newbie@example.com",
            "first_name": "Іван",
            "last_name": "Майстренко",
            "password1": "VerySafePass123!",
            "password2": "VerySafePass123!",
        },
    )
    assert response.status_code == 302
    assert User.objects.filter(username="newbie").exists()


@pytest.mark.django_db
def test_user_added_to_buyer_group_on_signup(buyer):
    assert buyer.groups.filter(name="Buyer").exists()


@pytest.mark.django_db
def test_seller_flag_after_profile_created(seller_profile):
    assert seller_profile.user.is_seller is True
    assert seller_profile.user.groups.filter(name="Seller").exists()

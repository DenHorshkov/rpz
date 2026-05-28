"""Спільні pytest-фікстури."""
from decimal import Decimal

import pytest
from django.contrib.auth import get_user_model

from apps.accounts.models import MasterProfile
from apps.catalog.models import Category, Product

User = get_user_model()


@pytest.fixture
def buyer(db):
    return User.objects.create_user(username="buyer", email="b@example.com", password="passw0rd!")


@pytest.fixture
def seller_user(db):
    return User.objects.create_user(username="seller", email="s@example.com", password="passw0rd!")


@pytest.fixture
def seller_profile(seller_user):
    return MasterProfile.objects.create(user=seller_user, display_name="Студія Хендмейд", city="Київ")


@pytest.fixture
def category(db):
    return Category.objects.create(name="Прикраси", slug="prykrasy")


@pytest.fixture
def product(seller_profile, category):
    return Product.objects.create(
        owner=seller_profile,
        category=category,
        title="Браслет з натурального каменю",
        description="Ручна робота",
        price=Decimal("350.00"),
        stock=5,
    )

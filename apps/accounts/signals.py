from django.conf import settings
from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import MasterProfile

BUYER_GROUP = "Buyer"
SELLER_GROUP = "Seller"


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def add_buyer_group(sender, instance, created, **kwargs) -> None:
    if not created:
        return
    group, _ = Group.objects.get_or_create(name=BUYER_GROUP)
    instance.groups.add(group)


@receiver(post_save, sender=MasterProfile)
def add_seller_group(sender, instance, created, **kwargs) -> None:
    if not created:
        return
    group, _ = Group.objects.get_or_create(name=SELLER_GROUP)
    instance.user.groups.add(group)

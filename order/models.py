import uuid
from random import randint
from django.db import models
from django.contrib.auth import get_user_model

from product.models import Product

User = get_user_model()


def get_order_number():
    return randint(1111, 9999)


def estimate_delivery_cost():
    return 5 * randint(1, 4)


class Item(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    amount = models.PositiveSmallIntegerField(null=False, blank=False)
    product = models.ForeignKey(
        to=Product, on_delete=models.CASCADE, null=False, blank=False, related_name="order_item")
    total_price = models.FloatField(null=False, blank=False)


class Order(models.Model):

    statuses = [
        ("pending", "Pending"),
        ("failed", "Failed"),
        ("success", "Success")
    ]
    owner = models.ForeignKey(
        to=User, on_delete=models.CASCADE, null=False, blank=False)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    number = models.IntegerField(
        default=get_order_number, unique=True, blank=False, null=False)
    address = models.TextField(null=False, blank=False)
    status = models.CharField(
        max_length=7,
        choices=statuses,
        null=False,
        blank=False
    )
    total_price = models.PositiveBigIntegerField(null=False, blank=False)
    delivery_cost = models.IntegerField(
        null=False, blank=False, default=estimate_delivery_cost)
    items = models.ForeignKey(
        to=Item, related_name="order", on_delete=models.CASCADE)

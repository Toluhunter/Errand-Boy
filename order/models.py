from uuid import uuid4
from random import randint
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

from product.models import Product

User = get_user_model()


def get_order_number():
    '''
    Generate a random 4-digit order number
    '''
    return randint(1111, 9999)


def estimate_delivery_cost():
    '''
    Generate Random delivery cost between 500 - 2000
    '''
    return 500 * randint(1, 4)


class Order(models.Model):

    statuses = [
        ("pending", "Pending"),
        ("accepted", "Accepted"), # Order accepted by courier
        ("failed", "Failed"),
        ("success", "Success")
    ]
    owner = models.ForeignKey(
        to=User, on_delete=models.CASCADE, null=False, blank=False)
    id = models.UUIDField(primary_key=True, default=uuid4)
    number = models.IntegerField(
        default=get_order_number, unique=True, blank=False, null=False)
    address = models.TextField(null=False, blank=False)
    instruction = models.TextField(null=False, blank=False)
    status = models.CharField(
        max_length=8,
        choices=statuses,
        null=False,
        blank=False,
        default="pending"
    )
    total_price = models.PositiveBigIntegerField(null=False, blank=False)
    delivery_cost = models.IntegerField(
        null=False, blank=False, default=estimate_delivery_cost)
    date_created = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-date_created"]

    def __str__(self) -> str:
        return f"{self.owner.last_name} {self.owner.first_name}--{self.total_price}--{self.date_created}"


class Item(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, blank=False)
    amount = models.PositiveSmallIntegerField(null=False, blank=False)
    product = models.ForeignKey(
        to=Product, on_delete=models.CASCADE, null=False, blank=False, related_name="order_item")
    total_price = models.FloatField(null=False, blank=False)  # Read only field
    order = models.ForeignKey(
        to=Order, related_name="items", on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"(Qty: {self.amount}), (Product Name: {self.product.name}), (Total Price: {self.total_price}), (Order ID: {self.order.id})"

import uuid
from django.db import models
from django.contrib.auth import get_user_model

from product.models import Product

User = get_user_model()


class Order(models.Model):

    statuses = [
        ("pending", "Pending"),
        ("failed", "Failed"),
        ("success", "Success")
    ]
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE, null=False, blank=False)
    number = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    address = models.TextField(null=False, blank=False)
    status = models.CharField(
        max_length=7,
        choices=statuses, 
        null=False, 
        blank=False
        )
    products = models.ManyToManyField(to=Product, related_name="orders")
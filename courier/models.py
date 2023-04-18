from django.db import models
from order.models import Order
from account.models import Account
from uuid import uuid4
from django.utils import timezone


class CourierOrder(models.Model):
    """Accepted order model"""
    id = models.UUIDField(default=uuid4, primary_key=True, unique=True)
    STATUSES = [
        ["pending", "Pending"],
        ["success", "Success"],
        ["failed", "Failed"],
    ]
    # Delivery to user status
    delivery_status = models.CharField(
        max_length=7, default="pending", blank=False, null=False, choices=STATUSES)

    courier = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name="courier")
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="courier_order")
    pay = models.PositiveBigIntegerField(blank=False, null=False)
    date_created = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-date_created"]

    def __str__(self):
        return f"{self.delivery_status} - {self.courier.last_name} {self.courier.first_name} - {self.pay}"
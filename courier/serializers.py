from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from courier.models import CourierOrder
from order.models import Order
from django.contrib.auth import get_user_model


class CreateCourierOrderSerializer(ModelSerializer):
    """Creates record when an order has been accepted."""
    order = serializers.PrimaryKeyRelatedField(queryset=Order.objects.all())
    courier = serializers.PrimaryKeyRelatedField(
        queryset=get_user_model().objects.all())

    class Meta:
        model = CourierOrder
        fields = ["courier", "order", "pay"]

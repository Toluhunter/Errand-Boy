from rest_framework import serializers
from .models import Order


class OrderSerializer(serializers.ModelSerializer):

    item = serializers.JSONField(required=True)

    class Meta:
        model = Order
        exclude = ['owner']

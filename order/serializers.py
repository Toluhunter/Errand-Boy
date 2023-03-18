from rest_framework import serializers
from .models import Order, Item


class OrderSerializer(serializers.ModelSerializer):

    item = serializers.JSONField(required=True)

    class Meta:
        model = Order
        exclude = ['owner']

    def create(self, validated_data):
        '''
        Creation of items and order instance
        '''
        ...

    def update(self, instance, validated_data):
        ...

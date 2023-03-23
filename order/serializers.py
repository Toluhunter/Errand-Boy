from rest_framework import serializers
from .models import Order, Item
from product.serializers import ProductSerializer


class ItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = Item
        fields = ["amount", "product"]


class CreateOrderSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ["address", "instruction"]

    def create(self, validated_data):
        '''
        Creation of items and order instance
        '''
        owner = self.context["request"].user
        validated_data["owner"] = owner

        items_data = validated_data.pop("items") # Removing products
        total_price = 0

        for item in items_data:
            # Calculate item total price
            total_price += (item.amount * item.product.price)

        validated_data["total_price"] = total_price
        order = Order.objects.create(**validated_data)  # Creating order

        # Creating items
        for item in items_data:
            total_price = item.amount * item.product.price
            Item.objects.create(order=order, product=item.product,
                                total_price=total_price, **item)

        return order


class OrderSerializer(serializers.ModelSerializer):
    pass
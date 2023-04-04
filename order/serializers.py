from rest_framework import serializers
from .models import Order, Item
from product.serializers import ProductIDSerializer, ProductSerializer


class ItemSerializer(serializers.ModelSerializer):
    """Serializer that represents Item"""
    product = ProductIDSerializer(required=True)

    class Meta:
        model = Item
        fields = ["amount", "product"]


class ItemDetailSerializer(serializers.ModelSerializer):
    """Serializer to fetch all Items in an order"""
    product = ProductSerializer(required=True)

    class Meta:
        model = Item
        fields = ["amount", "product"]


class CreateOrderSerializer(serializers.ModelSerializer):
    """Creation of order serializer"""
    items = ItemSerializer(many=True, required=True)

    class Meta:
        model = Order
        fields = ["items", "address", "instruction"]

    def validate(self, attrs):
        """
        Ensures that:
        1. An order contains an item.
        2. No repeating item is in contained in an order.
        """
        items = attrs["items"]

        if not items:
            raise serializers.ValidationError(
                {"error": "Order must contain at least an item."})

        product_ids = [item["product"]["product_id"] for item in items]
        # Using a set to remove duplicates
        set_product_ids = set(product_ids)

        # Checking for duplicate product ids
        if len(set_product_ids) != len(product_ids):
            raise serializers.ValidationError(
                {"error": "Duplicate product ID in items array."})

        return attrs

    def create(self, validated_data):
        '''
        Creation of items and order instance
        '''
        owner = self.context["request"].user
        validated_data["owner"] = owner

        items_data = validated_data.pop("items")  # Removing products
        total_price = 0

        # Calculate item total price
        for item in items_data:
            product = item["product"]["product"]
            total_price += (item["amount"] * product.price)

        validated_data["total_price"] = total_price
        order = Order.objects.create(**validated_data)  # Creating order

        # Creating items
        for item in items_data:
            product = item["product"]["product"]
            total_price = item["amount"] * product.price
            Item.objects.create(order=order, product=product,
                                total_price=total_price, amount=item["amount"])

        return order


class DetailOrderSerializer(serializers.ModelSerializer):
    """Get all order details serializer"""
    items = ItemDetailSerializer(many=True)

    class Meta:
        model = Order
        exclude = ["date_created", "owner"]

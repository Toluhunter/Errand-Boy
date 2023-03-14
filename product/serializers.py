from rest_framework import serializers
from .models import Product, Category


class ProductSerializer(serializers.ModelSerializer):

    product_id = serializers.CharField(read_only=True)
    category = serializers.PrimaryKeyRelatedField(
        required=True, queryset=Category.objects.all())

    class Meta:
        model = Product
        exclude = ["id", "foodservice"]

    def validate(self, attrs):
        category = attrs["category"]
        request = self.context["request"]

        if category.foodservice != request.user.foodservice:
            raise serializers.ValidationError(
                "Invalid Category For Foodservice")

        return attrs

    def create(self, validated_data):

        request = self.context["request"]
        foodservice = request.user.foodservice

        return self.Meta.model.objects.create(
            **validated_data, foodservice=foodservice)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if "name" in validated_data:
            instance.product_id = instance.set_product_id()

        instance.save()

        return instance


class CategortySerializer(serializers.ModelSerializer):

    id = serializers.UUIDField(read_only=True)

    class Meta:
        model = Category
        exclude = ["foodservice"]

    def create(self, validated_data):

        request = self.context["request"]
        foodservice = request.user.foodservice

        return self.Meta.model.objects.create(
            **validated_data, foodservice=foodservice)

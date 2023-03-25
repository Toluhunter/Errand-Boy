from rest_framework import serializers

from foodservice.serializers import FoodServiceSerializer
from .models import Product, Category


class CategortySerializer(serializers.ModelSerializer):
    '''
    Serializer to handle all CRUD operations for a Category
    '''

    id = serializers.UUIDField(read_only=True)

    class Meta:
        model = Category
        exclude = ["foodservice"]

    def validate(self, attrs):
        foodservice = self.context["request"].user.foodservice
        try:
            Category.objects.get(name=attrs["name"], foodservice=foodservice)
            raise serializers.ValidationError("Already Exisiting Category")
        except:
            pass
        return attrs

    def create(self, validated_data):

        request = self.context["request"]
        foodservice = request.user.foodservice

        return self.Meta.model.objects.create(
            **validated_data, foodservice=foodservice)


class ProductSerializer(serializers.ModelSerializer):
    '''
    Serializer to handle all CRUD operations for a product
    '''
    foodservice = FoodServiceSerializer(read_only=True)
    product_id = serializers.CharField(read_only=True)
    category = serializers.PrimaryKeyRelatedField(
        required=True, queryset=Category.objects.all())

    class Meta:
        model = Product
        exclude = ["id"]

    def __init__(self, instance=None, **kwargs):
        super().__init__(instance, **kwargs)
        if self.instance and "data" not in kwargs:
            self.fields["category"] = CategortySerializer(read_only=True)

    def validate(self, attrs):
        category = attrs["category"]
        request = self.context["request"]

        # only allow creation with category if owned by the food service
        if category.foodservice != request.user.foodservice:
            raise serializers.ValidationError(
                "Invalid Category For Foodservice")

        try:
            Product.objects.get(
                name=attrs["name"], foodservice=request.user.foodservice)
            raise serializers.ValidationError("Already Exisiting Product")
        except:
            pass

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
            # if product name is changed set set new user friendly product id
            instance.product_id = instance.set_product_id()

        instance.save()

        return instance


class ProductIDSerializer(serializers.Serializer):
    """Serializer for orders, allowing for linking with product ID"""
    id = serializers.IntegerField(required=True)

    def validate(self, attrs):
        try:
            product = Product.objects.get(id=attrs["id"])
        except Product.DoesNotExist:
            raise serializers.ValidationError(
                {"error": f"Product with id={attrs['id']} does not exist"})

        attrs[product] = product
        return attrs

    def save(self):
        return self.validated_data["product"]

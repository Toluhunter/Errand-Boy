from rest_framework import serializers
from .models import FoodService


class FoodServiceSerializer(serializers.ModelSerializer):
    '''
    Food Service Serializer to handle all CRUD operations
    '''

    class Meta:
        model = FoodService
        exclude = ["user"]
        read_only_fields = ["id"]

    def create(self, validated_data):
        return FoodService.objects.create(
            user=self.context["request"].user,
            **validated_data
        )

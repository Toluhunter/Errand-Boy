from rest_framework import serializers
from .models import FoodService


class FoodServiceSerializer(serializers.ModelSerializer):
    '''
    Food Service Serializer to handle all CRUD operations
    '''

    class Meta:
        model = FoodService
        exclude = ["user"]

    def __init__(self, instance=None, **kwargs):
        super().__init__(instance, **kwargs)

        # Sets id field to read only
        self.fields["id"].read_only = True

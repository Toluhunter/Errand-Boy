from rest_framework import serializers
from .models import FoodService

class FoodServiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = FoodService
        fields = '__all__'
    
    def __init__(self, instance=None, **kwargs):
        super().__init__(instance, **kwargs)
        self.fields["id"].read_only = True
        self.fields["user"].read_only = True
    
    def validate(self, attrs):
        attrs["user"] = self.context["request"].user

        return attrs

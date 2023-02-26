from django.shortcuts import get_object_or_404

from rest_framework import generics
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated


from .serializers import FoodServiceSerializer
from .permissions import Isowner
from account.permissions import IsFoodSevice
from .models import FoodService

class CreateFoodServiceVIew(generics.CreateAPIView):

    serializer_class = FoodServiceSerializer
    parser_classes = [MultiPartParser]
    permission_classes = [IsAuthenticated, IsFoodSevice]

class RetrieveFoodServiceView(generics.RetrieveAPIView):

    serializer_class = FoodServiceSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        id = self.kwargs["id"]
        obj = get_object_or_404(FoodService, id=id)

        self.check_object_permissions(request=self.request, obj=obj)

        return obj

class ManageFoodServiceView(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = FoodServiceSerializer
    permission_classes = [IsAuthenticated, IsFoodSevice, Isowner]
    parser_classes = [MultiPartParser]

    def get_object(self):
        id = self.kwargs["id"]
        obj = get_object_or_404(FoodService, id=id)

        self.check_object_permissions(request=self.request, obj=obj)

        return obj
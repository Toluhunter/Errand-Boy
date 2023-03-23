from django.shortcuts import get_object_or_404

from rest_framework import generics
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated


from .serializers import FoodServiceSerializer
from .permissions import Isowner
from account.permissions import IsFoodService, HasNotRegisteredFoodSevice
from .models import FoodService


class CreateFoodServiceVIew(generics.CreateAPIView):
    '''
    Class View to allow only users registered as food service to create a food service
    '''

    serializer_class = FoodServiceSerializer
    parser_classes = [MultiPartParser]
    permission_classes = [IsAuthenticated, HasNotRegisteredFoodSevice]


class ListFoodServiceView(generics.ListAPIView):
    serializer_class = FoodServiceSerializer
    queryset = FoodService.objects.all()
    permission_classes = [IsAuthenticated]


class RetrieveFoodServiceView(generics.RetrieveAPIView):
    '''
    Class View to allow any authenticated user view details of the food service
    '''

    serializer_class = FoodServiceSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        id = self.kwargs["id"]
        obj = get_object_or_404(FoodService, id=id)

        self.check_object_permissions(request=self.request, obj=obj)

        return obj
class RetrieveMyFoodServiceView(generics.RetrieveAPIView):
    '''
    Class View to allow any authenticated user view details of the food service
    '''

    serializer_class = FoodServiceSerializer
    permission_classes = [IsAuthenticated, IsFoodService]

    def get_object(self):
        obj = self.request.user.foodservice

        self.check_object_permissions(request=self.request, obj=obj)

        return obj

class ManageFoodServiceView(generics.RetrieveUpdateDestroyAPIView):
    '''
    Class view to allow only owner of the food service to perform all CRUD operations on it
    '''

    serializer_class = FoodServiceSerializer
    permission_classes = [IsAuthenticated, IsFoodService, Isowner]
    parser_classes = [MultiPartParser]

    def get_object(self):

        obj = self.request.user.foodservice
        self.check_object_permissions(request=self.request, obj=obj)

        return obj

from django.shortcuts import get_object_or_404

from rest_framework import generics, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser

from .serializers import ProductSerializer, CategortySerializer
from .permissions import IsProductOwner, IsCategoryOwner
from account.permissions import IsFoodService
from .models import Product, Category, FoodService


class CreateProductView(generics.CreateAPIView):
    '''
    Class View for adding a product by only a food service
    '''

    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, IsFoodService]
    parser_classes = [MultiPartParser]


class ListProductView(generics.ListAPIView):
    '''
    Class View for listing out all products added to the system, for authenticated users
    '''

    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    queryset = Product.objects.all()


class RetrieveProductView(generics.RetrieveAPIView):
    '''
    Class view for retrieving details of a particular product, for authenticated users
    '''
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        id = self.kwargs["id"]
        obj = get_object_or_404(Product, post_id=id)
        self.check_object_permissions(self.request, obj=obj)
        return obj


class ManageProductView(generics.GenericAPIView, mixins.UpdateModelMixin, mixins.DestroyModelMixin):

    '''
    Class view to handle updating and deleting of product details, by product owner
    '''
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, IsFoodService, IsProductOwner]

    def get_object(self):
        id = self.kwargs["id"]
        obj = get_object_or_404(Product, post_id=id)
        self.check_object_permissions(self.request, obj=obj)
        return obj

    def patch(self, request, **kwargs):
        return self.partial_update(request, **kwargs)

    def delete(self, request, **kwargs):
        return self.destroy(request, **kwargs)


class DeleteProductView(generics.DestroyAPIView):

    '''
    Class view for the deletion of product view by product owner
    '''

    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, IsFoodService, IsProductOwner]

    def get_object(self):
        id = self.kwargs["id"]

        obj = get_object_or_404(Product, post_id=id)

        self.check_object_permissions(self.request, obj=obj)

        return obj


class FetchFoodServiceProductView(generics.ListAPIView):
    '''
    Fetch all products added by the authenticated foodservice 
    '''

    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, IsFoodService]

    def get_queryset(self):
        filter = self.request.GET.get("filter", None)
        queryset = Product.objects.filter(
            foodservice=self.request.user.foodservice)
        if filter:
            queryset = queryset.filter(name__icontains=filter)

        return queryset


class AddCategoryView(generics.ListCreateAPIView):
    '''
    Class view to allow creation of a category belonging to a food service
    '''
    serializer_class = CategortySerializer
    permission_classes = [IsAuthenticated, IsFoodService]

    def get_queryset(self):
        return Category.objects.filter(foodservice=self.request.user.foodservice)


class ListCategoryView(generics.ListAPIView):
    '''
    For Review: Class View to allow authenticated user to fetch all categories
    '''
    serializer_class = CategortySerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        id = self.kwargs["id"]
        obj = get_object_or_404(FoodService, id=id)
        self.check_object_permissions(self.request, obj)
        return obj

    def get_queryset(self):

        foodservice = self.get_object()
        return Category.objects.filter(foodservice=foodservice)


class DeleteCategoryView(generics.DestroyAPIView):
    '''
    Class view to allow category owner delete category
    '''

    serializer_class = CategortySerializer
    permission_classes = [IsAuthenticated, IsFoodService, IsCategoryOwner]

    def get_object(self):
        id = self.kwargs["id"]

        obj = get_object_or_404(Category, id=id)

        self.check_object_permissions(self.request, obj=obj)

        return obj

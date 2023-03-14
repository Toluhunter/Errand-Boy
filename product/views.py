from django.shortcuts import get_object_or_404
from rest_framework import generics, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser

from .serializers import ProductSerializer, CategortySerializer
from .permissions import IsProductOwner, IsCategoryOwner
from account.permissions import IsFoodService
from .models import Product, Category


class CreateProductView(generics.CreateAPIView):

    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, IsFoodService]
    parser_classes = [MultiPartParser]


class ListProductView(generics.ListAPIView):

    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    queryset = Product.objects.all()


class RetrieveProductView(generics.RetrieveAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        id = self.kwargs["id"]
        obj = get_object_or_404(Product, post_id=id)

        self.check_object_permissions(self.request, obj=obj)

        return obj


class ManageProductView(generics.GenericAPIView, mixins.UpdateModelMixin, mixins.DestroyModelMixin):

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


class FetchFoodServiceProductView(generics.ListAPIView):

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
    serializer_class = CategortySerializer
    permission_classes = [IsAuthenticated, IsFoodService]

    def get_queryset(self):
        return Category.objects.filter(foodservice=self.request.user.foodservice)


class ListCategoryView(generics.ListAPIView):
    serializer_class = CategortySerializer
    permission_classes = [IsAuthenticated]
    queryset = Category.objects.all()


class DeleteCategoryView(generics.DestroyAPIView):

    serializer_class = CategortySerializer
    permission_classes = [IsAuthenticated, IsFoodService, IsCategoryOwner]

    def get_object(self):
        id = self.kwargs["id"]

        obj = get_object_or_404(Category, id=id)

        self.check_object_permissions(self.request, obj=obj)

        return obj


class DeleteProductView(generics.DestroyAPIView):

    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, IsFoodService, IsProductOwner]

    def get_object(self):
        id = self.kwargs["id"]

        obj = get_object_or_404(Product, post_id=id)

        self.check_object_permissions(self.request, obj=obj)

        return obj

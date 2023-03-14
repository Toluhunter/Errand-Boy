from rest_framework.permissions import BasePermission


class IsProductOwner(BasePermission):

    def has_object_permission(self, request, view, obj):

        return obj.foodservice == request.user.foodservice


class IsCategoryOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.foodservice == request.user.foodservice

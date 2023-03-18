from rest_framework.permissions import BasePermission


class IsProductOwner(BasePermission):
    '''
    Allow access only to food service that added the product
    '''

    def has_object_permission(self, request, view, obj):

        return obj.foodservice == request.user.foodservice


class IsCategoryOwner(BasePermission):
    '''
    Allow access only to food service that added the category
    '''

    def has_object_permission(self, request, view, obj):
        return obj.foodservice == request.user.foodservice

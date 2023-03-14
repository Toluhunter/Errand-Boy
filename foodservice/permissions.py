from rest_framework.permissions import BasePermission


class Isowner(BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user == obj.user


class IsFoodService(BasePermission):

    def has_permission(self, request, view):
        if request.user.role == request.user.FOODPROVIDER:
            try:
                request.user.foodservice
            except:
                return False
            return True

        return False

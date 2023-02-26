from rest_framework.permissions import BasePermission

class IsFoodSevice(BasePermission):

    def has_permission(self, request, view):
        
        return (request.user.role == request.user.FOODPROVIDER)

class IsCourier(BasePermission):

    def has_permission(self, request, view):
        
        return (request.user.role == request.user.COURIER)

class IsUser(BasePermission):

    def has_permission(self, request, view):
        
        return (request.user.role == request.user.USER)
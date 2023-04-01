from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    '''
    Allow access only to owner of the order
    '''

    def has_object_permission(self, request, view, obj):
        return request.user == obj.user


class IsOrderOwner(BasePermission):
    '''
    Allow access only to owner of the order with (obj=Order)
    '''

    def has_object_permission(self, request, view, obj):
        return request.user == obj.owner

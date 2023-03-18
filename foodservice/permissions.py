from rest_framework.permissions import BasePermission


class Isowner(BasePermission):
    '''
    Allow access only to owner of the food service
    '''

    def has_object_permission(self, request, view, obj):
        return request.user == obj.user

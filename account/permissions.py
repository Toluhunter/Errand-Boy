from rest_framework.permissions import BasePermission


class IsFoodService(BasePermission):

    def has_permission(self, request, view):
        if request.user.role == request.user.FOODPROVIDER:
            try:
                request.user.foodservice
            except:
                return False
            return True

        return False


class IsCourier(BasePermission):

    def has_permission(self, request, view):

        return (request.user.role == request.user.COURIER)


class IsUser(BasePermission):

    def has_permission(self, request, view):

        return (request.user.role == request.user.USER)


class HasNotRegisteredFoodSevice(BasePermission):
    '''
    Permission To check For Food Service Account that has no registered food service
    '''

    def has_permission(self, request, view):

        try:
            request.user.foodservice
        except:
            return request.user.role == request.user.FOODPROVIDER

        return False

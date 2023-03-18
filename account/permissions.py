from rest_framework.permissions import BasePermission


class IsFoodService(BasePermission):
    '''
    Allow Access only to users registered as food service with a registered food service
    '''

    def has_permission(self, request, view):
        if request.user.role == request.user.FOODPROVIDER:
            try:
                '''
                Checks if user has a registered food service
                '''
                request.user.foodservice
            except:
                return False
            return True

        return False


class IsCourier(BasePermission):
    '''
    Allow Access only to users registered as a courier
    '''

    def has_permission(self, request, view):

        return (request.user.role == request.user.COURIER)


class IsUser(BasePermission):

    def has_permission(self, request, view):

        return (request.user.role == request.user.USER)


class HasNotRegisteredFoodSevice(BasePermission):
    '''
    Allow access only to food service accounts that has no registered food service
    '''

    def has_permission(self, request, view):

        try:
            request.user.foodservice
        except:
            return request.user.role == request.user.FOODPROVIDER

        return False

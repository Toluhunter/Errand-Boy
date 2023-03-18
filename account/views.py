from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenViewBase
from . import serializers


class RegisterAccountView(generics.CreateAPIView):
    '''
    Class View to register user
    '''

    serializer_class = serializers.CreateAccountSerializer


class LoginView(TokenViewBase):

    '''
    Class View to authenticate and return user access and refresh token
    '''
    serializer_class = serializers.LoginSerializer


class AccountView(generics.RetrieveUpdateAPIView):
    '''
    Class View requiring authentication to edit and retrieve user details
    '''

    permission_classes = [IsAuthenticated]
    serializer_class = serializers.AccountSerializer

    def get_object(self):
        '''
        returns currently authenticated user for modifying or view details
        '''
        return self.request.user


class LogoutView(generics.GenericAPIView):
    '''
    Class View to blacklist users refresh token
    '''

    permission_classes = [IsAuthenticated]
    serializer_class = serializers.LogoutSerializer

    def post(self, request):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(status=status.HTTP_204_NO_CONTENT)


class RegisterFaceView(generics.CreateAPIView):
    '''
    Class View to registers user face
    '''
    serializer_class = serializers.RegisterFaceserializer
    permission_classes = [IsAuthenticated]


class FacialRecognitionLoginView(TokenViewBase):
    '''
    Class View to handle facial authentication
    '''

    serializer_class = serializers.FaceRecognitionLoginSerializer


class RefreshAccessTokenView(TokenViewBase):
    '''
    Class view to return new refresh and access tokens
    '''

    serializer_class = serializers.RefreshAccessSerializer

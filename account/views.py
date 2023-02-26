from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenViewBase
from .serializers import AccountSerializer, LoginSerializer, CreateAccountSerializer, LogoutSerializer, RefreshAccessSerializer

class RegisterAccountView(generics.CreateAPIView):

    serializer_class = CreateAccountSerializer


class LoginView(TokenViewBase):

    serializer_class = LoginSerializer

class AccountView(generics.RetrieveUpdateAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = AccountSerializer

    def get_object(self):

        return self.request.user

class LogoutView(generics.GenericAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = LogoutSerializer

    def post(self, request):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(status=status.HTTP_204_NO_CONTENT)

class RefreshAccessTokenView(TokenViewBase):
    
    serializer_class = RefreshAccessSerializer
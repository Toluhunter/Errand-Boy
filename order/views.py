from .serializers import OrderSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from account.permissions import IsUser
from rest_framework.generics import GenericAPIView


class CreateOrderView(GenericAPIView):
    """
    Creation of order by an authenticated user with ROLE=User.
    """
    permission_classes = [IsAuthenticated, IsUser]


class ListOrderView(GenericAPIView):
    """
    Retrieval of **all** orders page by an authenticated user with ROLE=User.
    """
    permission_classes = [IsAuthenticated, IsUser]


class OrderDetailView(GenericAPIView):
    """
    Retrieval of a **single** order by an authenticated user with ROLE=User.
    """
    permission_classes = [IsAuthenticated, IsUser]

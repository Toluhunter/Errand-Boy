from .serializers import (
    CreateOrderSerializer,
    ListOrderSerializer,
    DetailOrderSerializer
)
from rest_framework.permissions import IsAuthenticated
from account.permissions import IsUser
from .permissions import IsOwner, IsOrderOwner
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView
)
from .models import Order


class CreateOrderView(CreateAPIView):
    """
    Creation of order by an authenticated user with ROLE=User.
    """
    permission_classes = [IsAuthenticated, IsUser]
    serializer_class = CreateOrderSerializer


class ListOrderView(ListAPIView):
    """
    Retrieval of **all** orders owned by an authenticated user with ROLE=User.
    """
    permission_classes = [IsAuthenticated, IsUser, IsOwner]
    serializer_class = ListOrderSerializer
    queryset = Order.objects.all()


class OrderDetailView(RetrieveAPIView):
    """
    Retrieval of a **single** order by an authenticated user with ROLE=User.
    """
    permission_classes = [IsAuthenticated, IsUser, IsOrderOwner]
    serializer_class = DetailOrderSerializer
    queryset = Order.objects.all()

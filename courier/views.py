from courier.models import CourierOrder
from order.models import Order
from order.serializers import ListOrderSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from account.permissions import IsCourier
from rest_framework.generics import (
    CreateAPIView,
    GenericAPIView,
    ListAPIView
)
from rest_framework.views import APIView


class ListOrdersView(APIView):
    """List all pending user orders and *accepted pending* orders to ErrandBoi"""
    permission_classes = [IsAuthenticated, IsCourier]

    def get(self, request):
        # Get accept courier orders that are pending delivery
        courier_orders = CourierOrder.objects.filter(
            delivery_status="pending", courier=request.user)
        courier_orders = [order.order for order in courier_orders]
        courier_serializer = ListOrderSerializer(courier_orders, many=True)

        # Get all pending orders (un-accepted by any courier)
        orders = Order.objects.filter(status="pending")
        order_serializer = ListOrderSerializer(orders, many=True)

        # Create response
        data = {}
        data["pending_delivery"] = courier_serializer.data
        data["orders"] = order_serializer.data

        return Response(data, status=status.HTTP_200_OK)


class ListOrderHistoryView(APIView):
    """List order history for courier"""
    permission_classes = [IsAuthenticated, IsCourier]

    def get(self, request):
        # Get all courier orders
        orders = CourierOrder.objects.filter(courier=request.user)
        orders = [order.order for order in orders]
        order_serializer = ListOrderSerializer(orders, many=True)

        data = {}
        data["orders"] = order_serializer.data
        data["total_orders"] = len(data["orders"])
        return Response(data, status=status.HTTP_200_OK)


class AcceptOrderView(CreateAPIView):
    """
    Accept pending user order
    Steps:
    1. Change *order* status to --pending deliverly-- how??????
    2. Create a record in CourierOrder model
    """
    pass


class ConfirmPickupView(GenericAPIView):
    """View to enter code to *confirm* pickup of restaurant"""
    pass

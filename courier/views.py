from order.models import Order
from order.serializers import DetailOrderSerializer
from courier.serializers import CreateCourierOrderSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from account.permissions import IsCourier
from rest_framework import serializers
from rest_framework.generics import (
    GenericAPIView,
    ListAPIView
)


class ListUnacceptedOrdersView(ListAPIView):
    """List all pending orders(un-accepted orders)."""
    permission_classes = [IsAuthenticated, IsCourier]
    serializer_class = DetailOrderSerializer

    def get_queryset(self):
        return Order.objects.filter(status="pending")


class ListUnfulfilledOrdersView(ListAPIView):
    """List all accepted but unfulfilled orders."""
    permission_classes = [IsAuthenticated, IsCourier]
    serializer_class = DetailOrderSerializer

    def get_queryset(self):
        """Filter all unfullied orders belonging to a courier"""
        return Order.objects.filter(courier_order__delivery_status="pending",
                                    courier_order__courier=self.request.user)


class ListOrderHistoryView(ListAPIView):
    """List order history for courier"""
    permission_classes = [IsAuthenticated, IsCourier]
    serializer_class = DetailOrderSerializer

    def get_queryset(self):
        """Filter all fullied(failed or delivered) orders belonging to a courier"""
        return Order.objects.filter(courier_order__delivery_status__in=["success", "failed"],
                                    courier_order__courier=self.request.user)


class AcceptOrderView(GenericAPIView):
    """
    Accept pending user order
    Steps:
    1. Create a record in CourierOrder model
    """
    permission_classes = [IsAuthenticated, IsCourier]
    serializer_class = CreateCourierOrderSerializer

    def post(self, request, pk):
        """Create a courier order"""
        # Fetch order with key
        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            raise serializers.ValidationError({"error": "Invalid order id."})

        # Check if order has already been accepted
        if order.status == "accepted":
            raise serializers.ValidationError(
                {"error": "Cannot accept an already accepted order"})

        # Change order status
        order.status = "accepted"
        order.save()

        data = {
            "order": order.id,
            "pay": order.delivery_cost,
            "courier": request.user.id
        }

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        serializer.save()
        data = {
            "success": True,
            "message": "Order accepted",
            "order": order.id,
            "pay": order.delivery_cost
        }

        return Response(data, status=status.HTTP_200_OK)


class ConfirmDeliveryView(GenericAPIView):
    """View to enter code to *confirm* pickup of restaurant"""
    pass

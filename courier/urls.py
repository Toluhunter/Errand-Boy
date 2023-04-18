from django.urls import path
from .views import (
    ListUnfulfilledOrdersView,
    ListUnacceptedOrdersView,
    ListOrderHistoryView,
    AcceptOrderView,
    ConfirmDeliveryView,
)

app_name = "courier"

urlpatterns = [
    path("orders/unaccepted/", ListUnacceptedOrdersView.as_view(), name="unaccepted-orders"),
    path("orders/unfulfilled/", ListUnfulfilledOrdersView.as_view(), name="unfulfilled-order"),
    path("orders/history/", ListOrderHistoryView.as_view(), name="history"),
    path("accept/<uuid:pk>/", AcceptOrderView.as_view(), name="accept-order"),
]

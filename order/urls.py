from django.urls import path
from .views import (
    CreateOrderView,
    ListOrderView,
    OrderDetailView
)

app_name = "order"

urlpatterns = [
    path("create/", CreateOrderView.as_view(), name="create"),
    path("list/", ListOrderView.as_view(), name="list"),
    path("<UUID:pk>/", OrderDetailView.as_view(), name="detail")
]

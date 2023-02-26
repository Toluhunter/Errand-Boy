from django.urls import path

from . import views

app_name = "foodservice"

urlpatterns = [
    path("register/", views.CreateFoodServiceVIew.as_view(), name="register"),
    path("manage/<str:id>/", views.ManageFoodServiceView.as_view(), name="manage"),
    path("<str:id>/", views.RetrieveFoodServiceView.as_view(), name="retrieve")
]
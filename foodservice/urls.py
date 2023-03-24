from django.urls import path

from . import views

app_name = "foodservice"

urlpatterns = [
    path("register/", views.CreateFoodServiceVIew.as_view(), name="register"),
    path("manage/<uuid:id>/", views.ManageFoodServiceView.as_view(), name="manage"),
    path("all/", views.ListFoodServiceView.as_view(), name="list"),
    path("<uuid:id>/", views.RetrieveFoodServiceView.as_view(), name="retrieve"),
    path("", views.RetrieveMyFoodServiceView.as_view(), name="myfoodservice"),
]

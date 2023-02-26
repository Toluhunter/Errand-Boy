from django.urls import path
from . import views

app_name = "account"

urlpatterns = [
    path("register/", views.RegisterAccountView.as_view(), name="register"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("profile/", views.AccountView.as_view(), name="detail"),
    path("logout/", views.LogoutView.as_view(), name="logout")
]
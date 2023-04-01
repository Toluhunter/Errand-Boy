from django.urls import path
from . import views

app_name = "account"

urlpatterns = [
    path("register/", views.RegisterAccountView.as_view(), name="register"),
    path("register-face/", views.RegisterFaceView.as_view(), name="register-face"),
    path("face-login/", views.FacialRecognitionLoginView.as_view(), name="face-login"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("face-verify/", views.HasRegisteredFaceView.as_view(),
         name="face-verify"),
    path("profile/", views.AccountView.as_view(), name="detail"),
    path("logout/", views.LogoutView.as_view(), name="logout")
]

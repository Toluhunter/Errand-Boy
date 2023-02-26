from django.urls import path, include
from account.views import RefreshAccessTokenView

urlpatterns = [
    path("account/", include("account.urls")),
    path("token/refresh/", RefreshAccessTokenView.as_view()),
    path("foodservice/", include("foodservice.urls"))
]

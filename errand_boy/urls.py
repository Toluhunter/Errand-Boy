from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from account.views import RefreshAccessTokenView

urlpatterns = [
    path("account/", include("account.urls")),
    path("token/refresh/", RefreshAccessTokenView.as_view()),
    path("foodservice/", include("foodservice.urls")),
    path("product/", include("product.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

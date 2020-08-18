from django.urls import path

from cishe.api.fev1.auth.views import (
    TokenCookieDeleteView,
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path("token", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/delete", TokenCookieDeleteView.as_view(), name="token_delete"),
]

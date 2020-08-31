from django.urls import path

from cishe.api.fev1.auth.views import (
    TokenCookieDeleteView,
    TokenObtainPairView,
    TokenRefreshView,
    token_401,
    token_403,
    unauthorized_403,
)


urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/delete/", TokenCookieDeleteView.as_view(), name="token_delete"),
    path("token/token-403/", token_403, name="token_403"),
    path("token/unauthorized/", unauthorized_403, name="unauthorized_403"),
    path("token/token-401/", token_401, name="token_401"),
]

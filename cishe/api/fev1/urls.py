from django.urls import include, path

from cishe.api.v1.auth.views import HelloView

from .account import urls as account_urls
from .auth import urls as auth_urls
from .contract import urls as contract_urls


urlpatterns = [
    path("auth/", include((auth_urls, "auth"), namespace="auth")),
    path("account/", include((account_urls, "account"), namespace="account")),
    path("contract/", include((contract_urls, "contract"), namespace="contract")),
    path("hello/", HelloView.as_view(), name="hello"),
]

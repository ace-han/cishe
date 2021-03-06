from django.urls import include, path

from cishe.api.v1.auth.views import HelloView

from .account import urls as account_urls
from .auth import urls as auth_urls
from .comment import urls as comment_urls
from .common import urls as common_urls
from .contract import urls as contract_urls


urlpatterns = [
    path("auth/", include((auth_urls, "auth"), namespace="auth")),
    path("account/", include((account_urls, "account"), namespace="account")),
    path("contract/", include((contract_urls, "contract"), namespace="contract")),
    path("common/", include((common_urls, "common"), namespace="common")),
    path("comment/", include((comment_urls, "comment"), namespace="comment")),
    path("hello/", HelloView.as_view(), name="hello"),
]

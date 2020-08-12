from django.urls import include, path

from cishe.api.v1.auth.views import HelloView

from .auth import urls as auth_urls


urlpatterns = [
    path("auth", include((auth_urls, "auth"), namespace="auth")),
    path("hello/", HelloView.as_view(), name="hello"),
]

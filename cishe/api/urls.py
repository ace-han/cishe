from django.urls import include, path

from .fev1 import urls as fev1_urls
from .v1 import urls as v1_urls


urlpatterns = [
    # default is the latest
    path("", include((v1_urls, "default"), namespace="default")),
    path("fev1/", include((fev1_urls, "fev1"), namespace="fev1")),
    path("v1/", include((v1_urls, "v1"), namespace="v1")),
]

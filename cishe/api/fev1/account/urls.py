from django.urls import include, path
from rest_framework.routers import DefaultRouter

from cishe.api.fev1.account.views import UserViewSet


router = DefaultRouter()

router.register("users", UserViewSet)

urlpatterns = [
    path("", include(router.urls, "")),
]

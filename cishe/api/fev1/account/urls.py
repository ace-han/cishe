from django.urls import include, path
from rest_framework.routers import DefaultRouter

from cishe.api.fev1.account.views import GroupViewSet, UserViewSet


router = DefaultRouter()

router.register("users", UserViewSet)
router.register("groups", GroupViewSet)

urlpatterns = [
    path("", include(router.urls, "")),
]

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from cishe.api.fev1.account.views import GroupViewSet, UserViewSet


router = DefaultRouter()

router.register("users", UserViewSet, "user")
router.register("groups", GroupViewSet, "group")

urlpatterns = [
    path("", include(router.urls, "")),
]

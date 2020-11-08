from django.urls import include, path
from rest_framework.routers import DefaultRouter

from cishe.api.fev1.contract.views import (
    ContractViewSet,
    CustomerViewSet,
    ServiceInfoViewSet,
    TakeOverViewSet,
)


router = DefaultRouter()

router.register("contracts", ContractViewSet, "contract")
router.register("customers", CustomerViewSet)
router.register("services", ServiceInfoViewSet)
router.register("takeovers", TakeOverViewSet)

urlpatterns = [
    path("", include(router.urls, "")),
]

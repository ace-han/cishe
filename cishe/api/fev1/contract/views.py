from django.db.models.query import Prefetch
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from cishe.api.fev1.contract.filtersets import (
    ContractFilterSet,
    CustomerFilterSet,
    TakeOverFilterSet,
)
from cishe.api.fev1.contract.serializers import (
    CustomerSerializer,
    EditableContractSerializer,
    ServiceInfoSerializer,
    TakeOverSerializer,
)
from cishe.common.views import BulkDeleteMixin
from cishe.contract.models import Contract, Customer, ServiceInfo, TakeOver


class ContractViewSet(ModelViewSet, BulkDeleteMixin):
    serializer_class = EditableContractSerializer
    permission_classes = (IsAuthenticated,)
    filter_class = ContractFilterSet

    def get_queryset(self):
        qs = Contract.objects.prefetch_related(
            "customer",
            "sale_agent",
            "serviceinfo",
            Prefetch(
                "takeover_set", queryset=TakeOver.objects.order_by("-transfer_date")
            ),
        )
        return qs


class CustomerViewSet(ModelViewSet, BulkDeleteMixin):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    filter_class = CustomerFilterSet
    permission_classes = (IsAuthenticated,)
    search_fields = ["name", "phone_num"]


class ServiceInfoViewSet(ModelViewSet, BulkDeleteMixin):
    queryset = ServiceInfo.objects.all()
    serializer_class = ServiceInfoSerializer
    permission_classes = (IsAuthenticated,)


class TakeOverViewSet(ModelViewSet, BulkDeleteMixin):
    queryset = TakeOver.objects.all()
    serializer_class = TakeOverSerializer
    permission_classes = (IsAuthenticated,)
    filter_class = TakeOverFilterSet

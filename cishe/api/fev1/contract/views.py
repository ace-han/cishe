from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from cishe.api.fev1.contract.filtersets import CustomerFilterSet
from cishe.api.fev1.contract.serializers import (
    ContractSerializer,
    CustomerSerializer,
    ServiceInfoSerializer,
    TakeOverSerializer,
)
from cishe.contract.models import Contract, Customer, ServiceInfo, TakeOver


class ContractViewSet(ModelViewSet):
    serializer_class = ContractSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        qs = Contract.objects.prefetch_related("customer", "sale_agent", "serviceinfo")
        return qs


class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    filter_class = CustomerFilterSet
    permission_classes = (IsAuthenticated,)


class ServiceInfoViewSet(ModelViewSet):
    queryset = ServiceInfo.objects.all()
    serializer_class = ServiceInfoSerializer
    permission_classes = (IsAuthenticated,)


class TakeOverViewSet(ModelViewSet):
    queryset = TakeOver.objects.all()
    serializer_class = TakeOverSerializer
    permission_classes = (IsAuthenticated,)

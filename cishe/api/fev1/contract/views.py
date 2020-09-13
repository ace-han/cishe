from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from cishe.api.fev1.contract.serializers import (
    ContractSerializer,
    CustomerSerializer,
    ServiceInfoSerializer,
    TakeOverSerializer,
)
from cishe.contract.models import Contract, Customer, ServiceInfo, TakeOver


class ContractViewSet(ModelViewSet):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    permission_classes = (IsAuthenticated,)


class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = (IsAuthenticated,)


class ServiceInfoViewSet(ModelViewSet):
    queryset = ServiceInfo.objects.all()
    serializer_class = ServiceInfoSerializer
    permission_classes = (IsAuthenticated,)


class TakeOverViewSet(ModelViewSet):
    queryset = TakeOver.objects.all()
    serializer_class = TakeOverSerializer
    permission_classes = (IsAuthenticated,)

from rest_flex_fields import FlexFieldsModelSerializer
from rest_framework.serializers import ALL_FIELDS

from cishe.contract.models import Contract, Customer, ServiceInfo, TakeOver


class ContractSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Contract
        fields = ALL_FIELDS


class CustomerSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Customer
        fields = ALL_FIELDS


class ServiceInfoSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = ServiceInfo
        fields = ALL_FIELDS


class TakeOverSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = TakeOver
        fields = ALL_FIELDS

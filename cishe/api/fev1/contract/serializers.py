import arrow
from django.db.transaction import atomic
from rest_flex_fields import FlexFieldsModelSerializer
from rest_framework.serializers import ALL_FIELDS

from cishe.api.fev1.account.serializers import UserSerializer
from cishe.contract.models import Contract, Customer, ServiceInfo, TakeOver


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

    expandable_fields = {
        "counselor": (UserSerializer, {"source": "counselor"}),
    }


class ContractSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Contract
        fields = ALL_FIELDS

    expandable_fields = {
        "customer": (CustomerSerializer, {"source": "customer"}),
        "sale_agent": (UserSerializer, {"source": "sale_agent"}),
        "serviceinfo": (ServiceInfoSerializer, {"source": "serviceinfo"}),
        "takeovers": (TakeOverSerializer, {"source": "takeover_set", "many": True}),
    }


class EditableContractSerializer(ContractSerializer):
    @classmethod
    def prepare_contract_num(cls, validated_data, enrollment_semester: str) -> str:
        signing_branch = validated_data.get("signing_branch")
        if signing_branch == "广州" or not signing_branch:
            branch = "GZ"
        elif signing_branch == "北京":
            branch = "BJ"
        elif signing_branch == "珠海":
            branch = "ZH"
        else:
            branch = "X"
        signing_date = validated_data.get("signing_date")

        year_count = Contract.objects.filter(
            signing_date__year=arrow.utcnow().date().year
        ).count()
        result = "{}{}-{}-{:04d}".format(
            branch, f"{signing_date:%y}", enrollment_semester[:2], year_count
        )
        return result

    @atomic
    def create(self, validated_data):
        serviceinfo_data = self.initial_data.get("serviceinfo") or {}
        takeover_data = self.initial_data.pop("takeover") or {}

        contract_num = self.prepare_contract_num(
            validated_data, serviceinfo_data.get("enrollment_semester")
        )
        instance = Contract.objects.create(**validated_data, contract_num=contract_num)

        serviceinfo_data.update(
            {
                "contract": instance.id,
            }
        )
        s_ser = ServiceInfoSerializer(data=serviceinfo_data)
        s_ser.is_valid(raise_exception=True)
        s_ser.save()

        takeover_data.update(
            {
                "contract": instance.id,
            }
        )
        t_ser = TakeOverSerializer(data=takeover_data)
        t_ser.is_valid(raise_exception=True)
        t_ser.save()
        return instance

    @atomic
    def update(self, instance, validated_data):
        super().update(instance, validated_data)

        serviceinfo_data = self.initial_data.get("serviceinfo") or {}
        takeover_data = self.initial_data.pop("takeover") or {}

        s_ser = ServiceInfoSerializer(
            data=serviceinfo_data, instance=instance.serviceinfo
        )
        s_ser.is_valid(raise_exception=True)
        s_ser.save()

        if takeover_data:
            takeover_data.update(
                {
                    "contract": instance.id,
                }
            )
            t_ser = TakeOverSerializer(data=takeover_data)
            t_ser.is_valid(raise_exception=True)
            t_ser.save()
        return instance

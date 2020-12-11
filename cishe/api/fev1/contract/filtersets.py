import rest_framework_filters as filters
from django.db.models.query_utils import Q

from cishe.contract.models import Contract, Customer, TakeOver


class CustomerFilterSet(filters.FilterSet):
    phone_number__icontains = filters.CharFilter(method="filter_phone_number")

    class Meta:
        model = Customer
        fields = {
            "id": (
                "exact",
                "in",
            ),  # fore delete...
            "name": ("exact", "in", "icontains"),
            "university": ("exact", "in", "icontains"),
            "major": ("exact", "in", "icontains"),
        }

    def filter_phone_number(self, qs, field_name, value):
        # when it comes here, value will not be empty
        return qs.filter(
            Q(phone_num__icontains=value)
            | Q(phone_num2__icontains=value)
            | Q(parent_phone_num__icontains=value)
        )


class ContractFilterSet(filters.FilterSet):
    class Meta:
        model = Contract
        fields = {
            "id": (
                "exact",
                "in",
            ),  # fore delete...
            "contract_num": ("exact", "in", "icontains"),
        }


class TakeOverFilterSet(filters.FilterSet):
    class Meta:
        model = TakeOver
        fields = {
            "id": (
                "exact",
                "in",
            ),  # fore delete...
            "contract": (
                "exact",
                "in",
            ),
        }

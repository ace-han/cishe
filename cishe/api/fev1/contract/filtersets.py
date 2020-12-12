import rest_framework_filters as filters
from django.db.models.aggregates import Max
from django.db.models.expressions import F
from django.db.models.query_utils import Q

from cishe.common.filters import CharCSVFilter
from cishe.contract.models import Contract, Customer, ServiceInfo, TakeOver


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


class CharCSVOrFilter(CharCSVFilter):
    # refer to `ServiceInfoFilterSet`
    def filter(self, qs, value):
        q_obj = Q()
        expr = f"{self.field_name}__{self.lookup_expr}"
        for v in value:
            q_obj |= Q(**{expr: v})
        qs = qs.filter(q_obj)
        return qs


class ServiceInfoFilterSet(filters.FilterSet):
    # since `target_country_code` and `target_major` is comma separated fields
    # &target_country_code__oricontains=us,uk
    # =>
    # target_country_code__icontains=us or target_country_code__icontains=uk
    target_country_code__oricontains = CharCSVOrFilter(
        field_name="target_country_code", lookup_expr="icontains"
    )

    target_major__oricontains = CharCSVOrFilter(
        field_name="target_major", lookup_expr="icontains"
    )

    class Meta:
        model = ServiceInfo
        fields = {
            "id": (
                "exact",
                "in",
            ),
        }


class ContractFilterSet(filters.FilterSet):
    customer = filters.RelatedFilter(CustomerFilterSet, queryset=Customer.objects.all())

    serviceinfo = filters.RelatedFilter(
        ServiceInfoFilterSet, queryset=ServiceInfo.objects.all()
    )

    last_counselor__username__in = CharCSVFilter(
        method="filter_last_counselor_usernames"
    )

    class Meta:
        model = Contract
        fields = {
            "id": (
                "exact",
                "in",
            ),  # fore delete...
            "contract_num": ("exact", "in", "icontains"),
            "signing_date": ("gte", "lte", "range"),
            "probation_until": ("gte", "lte", "range"),
        }

    def filter_last_counselor_usernames(self, qs, field_name, value):
        qs = qs.annotate(max_transfer_date=Max("takeover__transfer_date")).filter(
            takeover__transfer_date=F("max_transfer_date"),
            takeover__counselor__username__in=value,
        )
        return qs


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

from django.contrib.auth.models import Group
from rest_framework_filters.filterset import FilterSet

from cishe.account.models import UserModel


class UserFilterSet(FilterSet):
    class Meta:
        model = UserModel
        fields = {
            "id": (
                "exact",
                "in",
            ),  # fore delete...
            "username": ("exact", "in", "icontains"),
            "first_name": ("exact", "in", "icontains"),
            "last_name": ("exact", "in", "icontains"),
            "email": ("exact", "in", "icontains"),
            "is_staff": ("exact",),
        }


class GroupFilterSet(FilterSet):
    class Meta:
        model = Group
        fields = {
            "id": (
                "exact",
                "in",
            ),  # fore delete...
            "name": ("exact", "in", "icontains"),
        }

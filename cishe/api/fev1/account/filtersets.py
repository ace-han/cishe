import rest_framework_filters as filters
from django.contrib.auth.models import Group

from cishe.account.models import UserModel


class GroupFilterSet(filters.FilterSet):
    class Meta:
        model = Group
        fields = {
            "id": (
                "exact",
                "in",
            ),  # fore delete...
            "name": ("exact", "in", "icontains"),
        }


class UserFilterSet(filters.FilterSet):
    groups = filters.RelatedFilter(GroupFilterSet, queryset=Group.objects.all())

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

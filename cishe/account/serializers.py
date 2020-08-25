from django.contrib.auth.models import Group
from rest_flex_fields import FlexFieldsModelSerializer
from rest_framework.serializers import ALL_FIELDS

from cishe.account.models import UserModel


class GroupSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Group
        fields = ALL_FIELDS


class UserSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = UserModel
        exclude = ("password",)


class UserGroupSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = UserModel
        exclude = ["password"]
        expandable_fields = {
            "groups": [GroupSerializer, {"source": "groups", "many": True}]
        }

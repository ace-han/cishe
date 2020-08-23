from rest_flex_fields import FlexFieldsModelSerializer
from rest_framework.fields import SerializerMethodField

from cishe.account.models import UserModel


class UserSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = UserModel
        exclude = ("password",)


class UserGroupSerializer(FlexFieldsModelSerializer):
    groups = SerializerMethodField()

    class Meta:
        model = UserModel
        exclude = ("password",)

    def get_groups(self, obj):
        # empty list for the time being
        return []

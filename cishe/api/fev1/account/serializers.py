from django.contrib.auth.models import Group
from django.db.transaction import atomic
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

    @atomic
    def create(self, validated_data):
        username = validated_data.pop("username")
        email = validated_data.pop("email", None)
        if not email:
            last_name = (validated_data.get("last_name") or username).lower()
            email = "{}.{}@helloedu.com".format(username, last_name)

        instance = UserModel.objects.create_user(
            username, email, username, **validated_data
        )
        return instance


class UserWithGroupSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = UserModel
        exclude = ["password"]
        expandable_fields = {
            "groups": (GroupSerializer, {"source": "groups", "many": True})
        }

    @atomic
    def create(self, validated_data):
        instance = super().create(validated_data)
        group_ids = self.initial_data.get("groups") or []
        if group_ids:
            group_qs = Group.objects.filter(id__in=group_ids)
            instance.groups.set(group_qs)
        return instance

    @atomic
    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        group_ids = self.initial_data.get("groups") or []
        if group_ids:
            group_qs = Group.objects.filter(id__in=group_ids)
            instance.groups.set(group_qs)
        return instance


class GroupWithUsersSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Group
        fields = ALL_FIELDS
        expandable_fields = {
            "users": (UserSerializer, {"source": "user_set", "many": True})
        }

    @atomic
    def create(self, validated_data):
        instance = super().create(validated_data)
        user_ids = self.initial_data.get("users") or []
        if user_ids:
            user_qs = UserModel.objects.filter(id__in=user_ids)
            instance.user_set.set(user_qs)
        return instance

    @atomic
    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        user_ids = self.initial_data.get("users") or []
        if user_ids:
            user_qs = UserModel.objects.filter(id__in=user_ids)
            instance.user_set.set(user_qs)
        return instance

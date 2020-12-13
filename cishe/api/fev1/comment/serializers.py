from django.contrib.contenttypes.models import ContentType
from rest_flex_fields import FlexFieldsModelSerializer
from rest_framework.fields import CharField, SerializerMethodField
from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.serializers import ALL_FIELDS

from cishe.account.models import UserModel
from cishe.comment.models import Comment


class ContentTypeSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = ContentType
        fields = ALL_FIELDS


class CommentSerializer(FlexFieldsModelSerializer):
    app_label = CharField(max_length=100, allow_blank=True, write_only=True)
    model = CharField(max_length=100, allow_blank=True, write_only=True)

    content_type = PrimaryKeyRelatedField(
        required=False, allow_null=True, queryset=ContentType.objects.all()
    )

    commented_user = SerializerMethodField()

    class Meta:
        model = Comment
        fields = ALL_FIELDS

    expandable_fields = {
        "content_type": (ContentTypeSerializer, {"source": "content_type"}),
    }

    def validate(self, attrs):
        if not attrs.get("content_type"):
            attrs["content_type"] = ContentType.objects.get(
                app_label=attrs.get("app_label"), model=attrs.get("model")
            )
        # no more use
        attrs.pop("app_label", None)
        attrs.pop("model", None)
        return attrs

    def get_commented_user(self, instance):
        qs = UserModel.objects.filter(username=instance.commented_by)
        if qs.exists():
            result = qs.values().get()
        else:
            result = {
                "id": 0,
                "username": instance.commented_by,
                "first_name": None,
                "last_name": None,
                "email": None,
            }
        return result

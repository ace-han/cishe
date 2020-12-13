import rest_framework_filters as filters
from django.contrib.contenttypes.models import ContentType

from cishe.comment.models import Comment


class ContentTypeFilter(filters.FilterSet):
    class Meta:
        model = ContentType
        fields = {
            "app_label": (
                "exact",
                "in",
            ),
            "model": (
                "exact",
                "in",
            ),
        }


class CommentFilterSet(filters.FilterSet):
    content_type = filters.RelatedFilter(
        ContentTypeFilter, queryset=ContentType.objects.all()
    )

    class Meta:
        model = Comment
        fields = {
            "id": (
                "exact",
                "in",
            ),  # fore delete...
            "object_id": ("exact", "in"),
            "removed": ("exact",),
        }

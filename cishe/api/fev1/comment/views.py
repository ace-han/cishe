from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from cishe.api.fev1.comment.filtersets import CommentFilterSet
from cishe.api.fev1.comment.serializers import CommentSerializer
from cishe.comment.models import Comment
from cishe.common.views import BulkDeleteMixin


class CommentViewSet(ModelViewSet, BulkDeleteMixin):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated,)
    filter_class = CommentFilterSet

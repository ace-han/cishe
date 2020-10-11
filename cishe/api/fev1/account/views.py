from django.contrib.auth.models import Group
from rest_flex_fields.utils import is_expanded
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from cishe.account.models import UserModel
from cishe.api.fev1.account.filtersets import GroupFilterSet, UserFilterSet
from cishe.api.fev1.account.permissions import (
    GroupPermissionFactory,
    IsSuperUser,
)
from cishe.api.fev1.account.serializers import (
    GroupWithUsersSerializer,
    UserSerializer,
    UserWithGroupSerializer,
)
from cishe.common.views import BulkDeleteMixin


class UserViewSet(ModelViewSet, BulkDeleteMixin):
    serializer_class = UserSerializer
    filter_class = UserFilterSet
    permission_classes = (IsAuthenticated | IsSuperUser,)

    def get_queryset(self):
        queryset = UserModel.objects.all()
        if is_expanded(self.request, "groups"):
            queryset = queryset.prefetch_related("groups")
        return queryset

    @action(detail=True, methods=("get",), url_path="user-info")
    def user_info(self, request, pk=None):
        # may go with groups
        obj = self.get_object()
        context = self.get_serializer_context()
        serializer = UserWithGroupSerializer(obj, context=context)
        return Response(serializer.data)

    @action(detail=False, methods=("get",), url_path="current-user-info")
    def current_user_info(self, request):
        # may go with groups
        context = self.get_serializer_context()
        serializer = UserWithGroupSerializer(request.user, context=context)
        return Response(serializer.data)


class GroupViewSet(ModelViewSet, BulkDeleteMixin):
    serializer_class = GroupWithUsersSerializer
    filter_class = GroupFilterSet
    search_fields = ["name"]
    permission_classes = (IsSuperUser | GroupPermissionFactory.create("supervisor"),)

    def get_queryset(self):
        queryset = Group.objects.prefetch_related("permissions")
        if is_expanded(self.request, "users"):
            queryset = queryset.prefetch_related(
                "user_set", "user_set__user_permissions", "user_set__groups"
            )
        return queryset

    @action(detail=True, methods=("post",), url_path="users")
    def set_users(self, request, pk=None):
        """When doing `post`, request.data['users'] = [id1, id2, ...]."""
        instance = self.get_object()

        if request.method.lower() == "post":
            user_ids = request.data.get("users")
            user_qs = UserModel.objects.filter(id__in=user_ids)
            instance.user_set.set(user_qs)
            queryset = user_qs
        else:
            queryset = instance.user_set.all()
        page = self.paginate_queryset(queryset)
        kwargs = {"context": self.get_serializer_context()}
        if page is not None:
            serializer = UserSerializer(page, many=True, **kwargs)
            return self.get_paginated_response(serializer.data)

        serializer = UserSerializer(queryset, many=True, **kwargs)
        return Response(serializer.data)

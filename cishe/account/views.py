from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from cishe.account.models import UserModel
from cishe.account.permissions import IsSuperUser
from cishe.account.serializers import UserGroupSerializer, UserSerializer


class UserViewSet(ModelViewSet):
    queryset = UserModel.objects.prefetch_related("groups")
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated | IsSuperUser,)

    @action(detail=True, methods=("get",), url_path="user-info")
    def user_info(self, request, pk=None):
        # may go with groups
        obj = self.get_object()
        context = self.get_serializer_context()
        serializer = UserGroupSerializer(obj, context=context)
        return Response(serializer.data)

    @action(detail=False, methods=("get",), url_path="current-user-info")
    def current_user_info(self, request):
        # may go with groups
        context = self.get_serializer_context()
        serializer = UserGroupSerializer(request.user, context=context)
        return Response(serializer.data)

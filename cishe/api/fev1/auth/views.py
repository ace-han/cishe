from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework_simplejwt.views import (
    TokenObtainPairView as OriginalTokenObtainPairView, 
    TokenRefreshView as OriginalTokenRefreshView
)


class HelloView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {"message": "Hello, World!"}
        return Response(content)


class TokenObtainPairView(OriginalTokenObtainPairView):
    token_refresh_view_name = 'api:fev1:auth:token_refresh'

    def post(self, request, *args, **kwargs):
        resp = super().post(request, *args, **kwargs)
        # empty the content
        resp.content = ''
        # we need it to be no content to avoid confidentials leak
        resp.status_code = status.HTTP_204_NO_CONTENT
        return resp


class TokenRefreshView(OriginalTokenRefreshView):
    token_refresh_view_name = 'api:fev1:auth:token_refresh'

    def post(self, request, *args, **kwargs):
        resp = super().post(request, *args, **kwargs)
        # empty the content
        resp.content = ''
        # we need it to be no content to avoid confidentials leak
        resp.status_code = status.HTTP_204_NO_CONTENT
        return resp


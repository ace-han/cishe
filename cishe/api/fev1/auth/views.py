from django.conf import settings
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import (
    TokenCookieDeleteView as OriginalTokenCookieDeleteView,
    TokenObtainPairView as OriginalTokenObtainPairView,
    TokenRefreshView as OriginalTokenRefreshView,
)


class HelloView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {"message": "Hello, World!"}
        return Response(content)


class TokenObtainPairView(OriginalTokenObtainPairView):
    token_refresh_view_name = "api:fev1:auth:token_refresh"

    def post(self, request, *args, **kwargs):
        resp = super().post(request, *args, **kwargs)
        # we use non-http cookie solution
        # since we use a few code from server side to control the expiration
        # and renewal of the `is_login` variable in sync
        # refer to
        # https://stackoverflow.com/questions/60826884/jwt-served-via-httponly-cookie-with-someway-to-find-out-is-logged-in
        cookie_data = self.get_cookie_data()
        cookie_data["httponly"] = False
        # though `cookie_data['expires']` equals to refresh_token,
        # `access_token` cookie expires as its encoded content indicates within
        # before cookie expiration !!!
        resp.set_cookie(
            settings.SIMPLE_JWT["AUTHENTICATED_COOKIE_KEY"], "true", **cookie_data
        )

        # empty the content
        resp.content = ""
        # we need it to be no content to avoid confidentials leak
        resp.status_code = status.HTTP_204_NO_CONTENT
        return resp


class TokenRefreshView(OriginalTokenRefreshView):
    token_refresh_view_name = "api:fev1:auth:token_refresh"

    def post(self, request, *args, **kwargs):
        resp = super().post(request, *args, **kwargs)
        # empty the content
        resp.content = ""
        # we need it to be no content to avoid confidentials leak
        resp.status_code = status.HTTP_204_NO_CONTENT
        return resp


class TokenCookieDeleteView(OriginalTokenCookieDeleteView):
    token_refresh_view_name = "api:fev1:auth:token_refresh"

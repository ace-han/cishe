import pytest
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken

from cishe.api.fev1.auth.views import HelloView, TokenRefreshView


@pytest.mark.django_db
@pytest.mark.count_queries(autouse=False)
def test_expired_or_invalid_access_token(rf):
    access_cookie_name = api_settings.AUTH_COOKIE
    request = rf.get("/api/fev1/hello/")
    request.COOKIES[access_cookie_name] = "random_access_token"
    view = HelloView.as_view()
    response = view(request)
    assert response.status_code == 403
    assert "code" in response.data


@pytest.mark.django_db
@pytest.mark.count_queries(autouse=False)
def test_unauthorized_access_token(rf):
    request = rf.get("/api/fev1/hello/")
    view = HelloView.as_view()
    response = view(request)
    assert response.status_code == 403
    assert "code" not in response.data


@pytest.mark.django_db
@pytest.mark.count_queries(autouse=False)
def test_invalid_or_expired_refresh_token(admin_user, rf):
    refresh_token_view = TokenRefreshView.as_view()
    refresh_cookie_name = TokenRefreshView.token_refresh_cookie_name
    invalid_refresh_token = "random_refresh_token"
    # content_type='application/json' is necessary and dont know why for the time being
    request = rf.post("/api/fev1/auth/token/refresh/", content_type="application/json")
    request.COOKIES[refresh_cookie_name] = invalid_refresh_token
    response = refresh_token_view(request)
    assert response.status_code == 401
    assert response.data["code"].code == "token_not_valid"


@pytest.mark.django_db
@pytest.mark.count_queries(autouse=False)
def test_blacklisted_refresh_token(admin_user, rf):
    refresh_token_view = TokenRefreshView.as_view()
    refresh_cookie_name = TokenRefreshView.token_refresh_cookie_name
    refresh = RefreshToken.for_user(admin_user)
    refresh_token = str(refresh)
    refresh.blacklist()
    # content_type='application/json' is necessary and dont know why for the time being
    request = rf.post("/api/fev1/auth/token/refresh/", content_type="application/json")
    request.COOKIES[refresh_cookie_name] = refresh_token

    response = refresh_token_view(request)
    assert response.status_code == 401
    assert response.data["code"].code == "token_not_valid"
    assert "blacklisted" in response.data["detail"]

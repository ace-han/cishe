import pytest
from django.contrib.auth.hashers import check_password


@pytest.mark.django_db
@pytest.mark.count_queries
def test_admin_user(admin_user):
    assert admin_user.email == "admin@example.com"
    assert check_password("admin", admin_user.password) is True

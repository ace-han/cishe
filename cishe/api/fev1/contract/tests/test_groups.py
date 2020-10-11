import pytest
from django.contrib.auth.models import Group

from cishe.api.fev1.account.views import GroupViewSet


@pytest.mark.django_db
@pytest.mark.count_queries(autouse=False)
def test_group_with_users(supervisor_group, sunny_user):
    # I need to declare `sunny_user` to get `sunny_user` persistent into runtime db
    group_user_qs = supervisor_group.user_set.filter(username=sunny_user.username)
    assert group_user_qs.exists()

    # related_name
    group = Group.objects.prefetch_related("user_set").get(name=supervisor_group.name)
    assert group.user_set.get(username="sunny").id == sunny_user.id

    # related_query_name
    # given UserModel groups = models.ManyToManyField(Group, related_query_name='user')
    assert Group.objects.filter(user__username=sunny_user.username).exists()


@pytest.mark.django_db
@pytest.mark.count_queries(autouse=False)
def test_group_viewset_is_secured(sunny_user, luey_user, rf, operation_group):
    # declare `operation_group` to get operation_group init-ed
    request = rf.get("/api/fev1/account/groups/")
    request.user = luey_user
    group_mgt_view = GroupViewSet.as_view({"get": "list"})
    response = group_mgt_view(request)
    assert response.status_code == 403

    request.user = sunny_user
    response = group_mgt_view(request)
    assert response.status_code == 200

# since using pytest-factoryboy here is usually the factory fixture only
import factory
import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group
from factory.django import DjangoModelFactory
from pytest_factoryboy import register


UserModel = get_user_model()


class GroupFactory(DjangoModelFactory):
    class Meta:
        model = Group

    name = factory.Sequence(lambda n: "Group #%s" % n)


class UserFactory(DjangoModelFactory):
    class Meta:
        model = UserModel

    is_superuser = False
    is_staff = True
    username = factory.Sequence(lambda n: "user_{}".format(n))
    email = factory.LazyAttribute(lambda u: "{}@example.com".format(u.username))
    password = factory.LazyAttribute(lambda u: make_password(u.username))

    # https://pytest-factoryboy.readthedocs.io/en/latest/#post-generation-dependencies
    @factory.post_generation
    def groups(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return
        if extracted:
            # A list of groups were passed in, use them
            for group in extracted:
                # Assert that group is evaluated before user generation
                assert group.name is not None
                self.groups.add(group)


register(GroupFactory)  # group, group_factory
register(UserFactory)  # user, user_factory

register(GroupFactory, "admin_group", name="admin")
register(GroupFactory, "sales_group", name="sales")
register(GroupFactory, "operation_group", name="operation")
register(GroupFactory, "supervisor_group", name="supervisor")
register(GroupFactory, "visitor_group", name="visitor")

# register(UserFactory, 'admin_user', **{
#     'username': 'admin',
#     'is_superuser': True,
#     'groups': [LazyFixture("admin_group")]
# })


@pytest.fixture
def admin_user(admin_group):
    # since above register usage for many2many is not working
    # we might as well do it this way
    return UserFactory.create(username="admin", is_superuser=True, groups=[admin_group])


# register(UserFactory, 'sunny_user', **{
#     'username': 'sunny',
#     'groups': [
#         LazyFixture("supervisor_group"),
#         LazyFixture("operation_group"),
#     ]
# })


@pytest.fixture
def sunny_user(supervisor_group, operation_group):
    # since above register usage for many2many is not working
    # we might as well do it this way
    return UserFactory.create(
        username="sunny", groups=[supervisor_group, operation_group]
    )


@pytest.fixture
def luey_user(operation_group):
    # since above register usage for many2many is not working
    # we might as well do it this way
    return UserFactory.create(username="luey", groups=[operation_group])

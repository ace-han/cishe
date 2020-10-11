from rest_framework.permissions import BasePermission, IsAdminUser


class IsStaffUser(IsAdminUser):
    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class IsSuperUser(BasePermission):
    """Allows access only to admin users."""

    def has_permission(self, request, view):
        return request.user and request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class GroupBasedPermission(BasePermission):
    group_name = "specific_group_name"

    def has_permission(self, request, view):
        if request.user:
            return request.user.groups.filter(name=self.group_name).exists()
        else:
            False

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class GroupPermissionFactory(object):
    @staticmethod
    def create(group_name) -> type:
        clazz = type(
            "{}GroupPermission".format(group_name),
            (GroupBasedPermission,),
            {"group_name": group_name},
        )
        return clazz

from rest_framework.permissions import BasePermission


def is_group_member(user, *groups):
    assert len(groups) > 0, 'You must provide at least one group name'

    if not hasattr(user, 'groups'):
        return False  # swapped user model, doesn't support groups
    if not hasattr(user, '_group_names_cache'):  # pragma: no cover
        user._group_names_cache = set(
            user.groups.values_list('name', flat=True))

    return set(groups).issubset(user._group_names_cache)


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return is_group_member(request.user, 'admin')

    def has_object_permission(self, request, view, obj):
        return is_group_member(request.user, 'admin')


class IsGeneralUser(BasePermission):
    def has_permission(self, request, view):
        return is_group_member(request.user, 'general_user')

    def has_object_permission(self, request, view, obj):
        return is_group_member(request.user, 'general_user')

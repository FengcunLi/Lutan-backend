from rest_framework.permissions import BasePermission

object_level_permissions_self = (
    ('can_delete_this_thread', 'can delete this thread'),
    ('can_change_this_thread', 'can change this thread'),
    ('can_view_this_thread', 'can view this thread'),
    ('can_pin_this_thread', 'can pin thread this thread'),
    ('can_hide_this_thread', 'can hide this thread'),
    ('can_close_this_thread', 'can close this thread'),
    ('can_approve_this_thread', 'can approve this thread')
)


class CanDeleteThisThread(BasePermission):
    def has_object_permission(self, request, view, thread):
        return request.user.has_perm('can_delete_this_thread', thread)


class CanChangeThisThread(BasePermission):
    def has_object_permission(self, request, view, thread):
        return request.user.has_perm('can_change_this_thread', thread)


class CanViewThisThread(BasePermission):
    def has_object_permission(self, request, view, thread):
        return request.user.has_perm('can_view_this_thread', thread)


class CanPinThisThread(BasePermission):
    def has_object_permission(self, request, view, thread):
        return request.user.has_perm('can_pin_this_thread', thread)


class CanHideThisThread(BasePermission):
    def has_object_permission(self, request, view, thread):
        return request.user.has_perm('can_hide_this_thread', thread)


class CanCloseThisThread(BasePermission):
    def has_object_permission(self, request, view, thread):
        return request.user.has_perm('can_close_this_thread', thread)


class CanApproveThisThread(BasePermission):
    def has_object_permission(self, request, view, thread):
        return request.user.has_perm('can_approve_this_thread', thread)

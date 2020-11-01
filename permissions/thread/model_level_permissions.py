from rest_framework.permissions import BasePermission

model_level_permissions = (
    ('can_start_thread_globally', 'can start thread globally'),
    ('can_delete_thread_globally', 'can delete globally'),
    ('can_change_thread_globally', 'can change globally'),
    ('can_view_thread_globally', 'can view globally'),
    ('can_pin_thread_globally', 'can pin thread globally'),
    ('can_hide_thread_globally', 'can hide globally'),
    ('can_close_thread_globally', 'can close globally'),
    ('can_approve_thread_globally', 'can approve globally'),
    ('can_merge_thread_globally', 'can merge thread globally')
)


class CanStartThreadGlobally(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('can_start_thread_globally')


class CanDeleteThreadGlobally(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('can_delete_thread_globally')


class CanChangeThreadGlobally(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('can_change_thread_globally')


class CanViewThreadGlobally(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('can_view_thread_globally')


class CanPinThreadGlobally(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('can_pin_thread_globally')


class CanHideThreadGlobally(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('can_hide_thread_globally')


class CanCloseThreadGlobally(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('can_close_thread_globally')


class CanApproveThreadGlobally(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('can_approve_thread_globally')
# TODO:can_merge_thread_globally

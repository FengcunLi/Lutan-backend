from rest_framework.permissions import BasePermission

model_level_permissions = (
    ('can_add_post_globally', 'can add post globally'),
    ('can_delete_post_globally', 'can delete post globally'),
    ('can_change_post_globally', 'can change post globally'),
    ('can_view_post_globally', 'can view post globally'),
    ('can_hide_post_globally', 'can hide post globally'),
    ('can_approve_post_globally', 'can approve post globally'),
    ('can_merge_post_globally', 'can merge post globally'),
    ('can_like_post_globally', 'can like post globally')
)


class CanAddPostGlobally(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('can_add_post_globally')


class CanDeletePostGlobally(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('can_delete_post_globally')


class CanChangePostGlobally(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('can_change_post_globally')


class CanViewPostGlobally(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('can_view_post_globally')


class CanHidePostGlobally(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('can_hide_post_globally')


class CanApprovePostGlobally(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('can_approve_post_globally')


class CanLikePostGlobally(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('can_like_post_globally')

# TODO:can_merge_post_globally

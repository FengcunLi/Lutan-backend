from django.apps import apps
from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import BasePermission

object_level_permissions_in_thread = (
    ('can_add_post_in_this_thread', 'can add post of this thread'),
    ('can_delete_post_in_this_thread', 'can delete post of this thread'),
    ('can_change_post_in_this_thread', 'can change post of this thread'),
    ('can_view_post_in_this_thread', 'can view post of this thread'),
    ('can_hide_post_in_this_thread', 'can hide post of this thread'),
    ('can_approve_post_in_this_thread', 'can approve post of this thread'),
    ('can_merge_post_in_this_thread', 'can merge post of this thread'),
    ('can_like_post_in_this_thread', 'can like post of this thread')
)


class CanAddPostInThisThread(BasePermission):
    def has_permission(self, request, view):
        Thread = apps.get_model(app_label='threads', model_name='Thread')

        thread_pk = request.data.get('thread', None)

        if thread_pk is None:
            raise serializers.ValidationError('thread was not provided')

        try:
            thread = Thread.objects.get(pk=thread_pk)
        except:
            raise serializers.ValidationError('thread was invalid')

        return request.user.has_perm('can_add_post_in_this_thread', thread)


class CanDeletePostInThisThread(BasePermission):
    def has_object_permission(self, request, view, post):
        return request.user.has_perm('can_delete_post_in_this_thread', post.thread)


class CanChangePostInThisThread(BasePermission):
    def has_object_permission(self, request, view, post):
        return request.user.has_perm('can_change_post_in_this_thread', post.thread)


class CanViewPostInThisThread(BasePermission):
    def has_object_permission(self, request, view, post):
        return request.user.has_perm('can_view_post_in_this_thread', post.thread)


class CanHidePostInThisThread(BasePermission):
    def has_object_permission(self, request, view, post):
        return request.user.has_perm('can_hide_post_in_this_thread', post.thread)


class CanApprovePostInThisThread(BasePermission):
    def has_object_permission(self, request, view, post):
        return request.user.has_perm('can_approve_post_in_this_thread', post.thread)


class CanLikePostInThisThread(BasePermission):
    def has_permission(self, request, view):
        post_pk = view.kwargs.get('pk', None)

        Post = apps.get_model(app_label='posts', model_name='Post')
        queryset = Post.objects.select_related('thread').all()

        post = get_object_or_404(queryset, pk=post_pk)

        return request.user.has_perm('can_like_post_in_this_thread', post.thread)

# TODO:can_merge_post_in_this_thread

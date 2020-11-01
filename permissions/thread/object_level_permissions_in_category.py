from django.apps import apps
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import BasePermission

object_level_permissions_in_category = (
    ('can_start_thread_in_this_category', 'can start thread in this category'),
    ('can_delete_thread_in_this_category', 'can delete thread in this category'),
    ('can_change_thread_in_this_category', 'can change thread in this category'),
    ('can_view_thread_in_this_category', 'can view thread in this category'),
    ('can_pin_thread_in_this_category', 'can pin thread in this category'),
    ('can_hide_thread_in_this_category', 'can hide thread in this category'),
    ('can_close_thread_in_this_category', 'can close thread in this category'),
    ('can_approve_thread_in_this_category', 'can approve thread in this category'),
    ('can_merge_thread_in_this_category', 'can merge thread in this category'),
)


class CanStartThreadInThisCategory(BasePermission):
    def has_permission(self, request, view):
        Category = apps.get_model(
            app_label='categories', model_name='Category')

        category_pk = request.data.get("category", None)

        if category_pk is None:
            raise serializers.ValidationError('category was not provided')

        try:
            category = Category.objects.get(pk=category_pk)
        except:
            raise serializers.ValidationError('category was invalid')

        return request.user.has_perm('can_start_thread_in_this_category', category)


class CanDeleteThreadInThisCategory(BasePermission):
    def has_object_permission(self, request, view, thread):
        return request.user.has_perm('can_delete_thread_in_this_category', thread.category)


class CanChangeThreadInThisCategory(BasePermission):
    def has_object_permission(self, request, view, thread):
        return request.user.has_perm('can_change_thread_in_this_category', thread.category)


class CanViewThreadInThisCategory(BasePermission):
    def has_object_permission(self, request, view, thread):
        return request.user.has_perm('can_view_thread_in_this_category', thread.category)


class CanListThreadInThisCategory(BasePermission):
    def has_permission(self, request, view):
        Category = apps.get_model(
            app_label='categories', model_name='Category')

        categories = request.query_params.get("categories", None)
        if categories is not None:
            categories = categories.split(",")
            categories_clean = []
            for category in categories:
                try:
                    categories_clean.append(int(category))
                except:
                    pass
            queryset = Category.objects.filter(id__in=categories_clean)
        else:
            queryset = Category.objects.all()

        forbidden = []
        categories = list(queryset)
        for category in categories:
            if not request.user.has_perm('can_view_thread_in_this_category', category):
                forbidden.append(category.id)

        if len(categories) > 0 and len(forbidden) > 0:
            raise PermissionDenied(
                detail='You do not have permission to view threads in categories: %s.' % forbidden)
        else:
            return True


class CanPinThreadInThisCategory(BasePermission):
    def has_object_permission(self, request, view, thread):
        return request.user.has_perm('can_pin_thread_in_this_category', thread.category)


class CanHideThreadInThisCategory(BasePermission):
    def has_object_permission(self, request, view, thread):
        return request.user.has_perm('can_hide_thread_in_this_category', thread.category)


class CanCloseThreadInThisCategory(BasePermission):
    def has_object_permission(self, request, view, thread):
        return request.user.has_perm('can_close_thread_in_this_category', thread.category)


class CanApproveThreadInThisCategory(BasePermission):
    def has_object_permission(self, request, view, thread):
        return request.user.has_perm('can_approve_thread_in_this_category', thread.category)


# TODO
# can_merge_thread_in_this_category

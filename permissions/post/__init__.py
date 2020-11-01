from rest_framework.permissions import BasePermission

from .model_level_permissions import *
from .object_level_permissions_in_category import *
from .object_level_permissions_in_thread import *


class IsPoster(BasePermission):
    def has_object_permission(self, request, view, post):
        return request.user.id == post.poster_id

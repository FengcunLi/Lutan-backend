from rest_framework.permissions import BasePermission

from .model_level_permissions import *
from .object_level_permissions_in_category import *
from .object_level_permissions_self import *


class IsStarter(BasePermission):
    def has_object_permission(self, request, view, thread):
        return request.user.id == thread.starter_id

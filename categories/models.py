from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

from permissions.category import model_level_permissions
from permissions.post import \
    object_level_permissions_in_category as \
    post_object_level_permissions_in_category
from permissions.thread import \
    object_level_permissions_in_category as \
    thread_object_level_permissions_in_category


class Category(MPTTModel):
    parent = TreeForeignKey(
        "self", null=True, blank=True, related_name="children", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=255, null=False,
                            blank=False, unique=True)
    description = models.TextField(null=True, blank=True)
    is_closed = models.BooleanField(default=False)
    require_threads_approval = models.BooleanField(default=False)
    require_posts_approval = models.BooleanField(default=False)

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name_plural = "categories"

        permissions = model_level_permissions + post_object_level_permissions_in_category + \
            thread_object_level_permissions_in_category
        default_permissions = ()

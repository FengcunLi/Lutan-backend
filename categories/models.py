from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


class Category(MPTTModel):
    parent = TreeForeignKey(
        "self", null=True, blank=True, related_name="children", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    is_closed = models.BooleanField(default=False)
    require_threads_approval = models.BooleanField(default=False)
    require_posts_approval = models.BooleanField(default=False)

    def __str__(self):
        return str(self.name)

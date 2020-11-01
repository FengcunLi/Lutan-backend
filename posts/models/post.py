from django.conf import settings
# from django.contrib.postgres.search import SearchVector, SearchVectorField
from django.db import models
from django.utils import timezone
from mptt.models import MPTTModel, TreeForeignKey

from permissions.post import model_level_permissions
from threads.models.thread import Thread


class Post(MPTTModel):
    parent = TreeForeignKey(
        "self", null=True, blank=True, related_name="children", on_delete=models.CASCADE
    )
    thread = models.ForeignKey(Thread,
                               on_delete=models.CASCADE, related_name='posts')
    poster = models.ForeignKey(settings.AUTH_USER_MODEL,
                               null=True,
                               on_delete=models.SET_NULL,
                               related_name='posts')
    content = models.TextField()

    is_unapproved = models.BooleanField(default=False, db_index=True)
    # No user will see this post if is_hidden equals True
    is_hidden = models.BooleanField(default=False, db_index=True)

    # search_document = models.TextField(null=True, blank=True)
    # search_vector = SearchVectorField()

    created_on = models.DateTimeField(default=timezone.now, db_index=True)

    def __str__(self):
        return "%s..." % self.content[10:].strip()

    class Meta:
        permissions = model_level_permissions
        default_permissions = ()

from django.conf import settings
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVectorField
from django.db import models
from django.db.models import Q
from django.utils import timezone

from categories.models import Category
from permissions.post import object_level_permissions_in_thread
from permissions.thread import (model_level_permissions,
                                object_level_permissions_self)


class Thread(models.Model):
    WEIGHT_DEFAULT = 0
    WEIGHT_PINNED_LOCALLY = 1
    WEIGHT_PINNED_GLOBALLY = 2
    WEIGHT_CHOICES = dict([
        (WEIGHT_DEFAULT, "Don't pin thread"),
        (WEIGHT_PINNED_LOCALLY, "Pin thread within category"),
        (WEIGHT_PINNED_GLOBALLY, "Pin thread globally"),
    ])

    title = models.CharField(max_length=255)
    content = models.TextField(null=True, blank=True)

    # Managed automatically by trigger, see threads.migrations.*create_trigger
    title_search_vector = SearchVectorField(null=True)
    content_search_vector = SearchVectorField(null=True)

    weight = models.PositiveIntegerField(default=WEIGHT_DEFAULT,
                                         choices=WEIGHT_CHOICES.items())
    is_unapproved = models.BooleanField(default=False, db_index=True)
    # No user will see this thread if is_hidden equals True
    is_hidden = models.BooleanField(default=False, db_index=True)
    # No user can comment this thread if is_closed equals True
    is_closed = models.BooleanField(default=False, db_index=True)

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    starter = models.ForeignKey(settings.AUTH_USER_MODEL,
                                null=True,
                                on_delete=models.SET_NULL,
                                related_name='threads')
    created_on = models.DateTimeField(default=timezone.now, db_index=True)

    # Managed automatically by trigger, see posts.migrations.*create_trigger
    last_post_created_on = models.DateTimeField(default=None,
                                                null=True,
                                                db_index=True)

    class Meta:
        indexes = [
            models.Index(
                name="thread_pinned_globally",
                fields=["weight"],
                condition=Q(weight=2),
            ),
            models.Index(
                name="thread_pinned_locally",
                fields=["weight"],
                condition=Q(weight=1),
            ),
            models.Index(
                name="thread_not_pinned",
                fields=["weight"],
                condition=Q(weight=0),
            ),
            GinIndex(fields=['title_search_vector', 'content_search_vector'])
        ]

        index_together = [
            ["category", "id"],
        ]

        permissions = model_level_permissions + \
            object_level_permissions_self + object_level_permissions_in_thread
        default_permissions = ()

    def __str__(self):
        return self.title

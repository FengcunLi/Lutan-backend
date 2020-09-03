from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields.jsonb import JSONField
from django.db import models
from django.utils.translation import gettext_lazy as _

from avatars import upload_to


class User(AbstractUser):
    """Lutan User Model Class

    User.is_staff: 
        Designates whether the user can log into admin sites.
    User.is_active: 
        Designates whether this user should be treated as active.
        Unselect this instead of deleting accounts.

    Args:
        models ([type]): [description]
    """

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']
    email = models.EmailField(
        _('email address'), null=False, blank=False, unique=True)

    avatar_tmp = models.ImageField(
        max_length=255, upload_to=upload_to, null=True, blank=True
    )
    avatar_src = models.ImageField(
        max_length=255, upload_to=upload_to, null=True, blank=True
    )
    avatar_crop = models.CharField(max_length=255, null=True, blank=True)
    avatars = JSONField(null=True, blank=True)

    signature = models.CharField(max_length=255, null=True, blank=True)

    followings = models.ManyToManyField(
        "self", related_name="followers", symmetrical=False,
    )

    blockings = models.ManyToManyField(
        "self", related_name="blockers", symmetrical=False
    )


class UserProxy(User):
    class Meta:
        proxy = True

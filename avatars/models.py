import os
from hashlib import md5

from django.conf import settings
from django.db import models
from django.utils.crypto import get_random_string


def upload_to(instance, filename):
    spread_path = md5(get_random_string(64).encode()).hexdigest()
    filename_clean = "%s.png" % get_random_string(32)

    return os.path.join(
        "avatars", spread_path[:2], spread_path[2:4], filename_clean
    )


class Avatar(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, related_name='avatars')

    width = models.PositiveIntegerField(null=True)
    height = models.PositiveIntegerField(null=True)
    image = models.ImageField(
        width_field='width', height_field='height', upload_to=upload_to)

    original = models.BooleanField(default=True)

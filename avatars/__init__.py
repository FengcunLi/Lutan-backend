import os
from hashlib import md5

from django.utils.crypto import get_random_string


def upload_to(instance, filename):
    spread_path = md5(get_random_string(64).encode()).hexdigest()
    secret = get_random_string(32)
    filename_clean = "%s.png" % get_random_string(32)

    return os.path.join(
        "avatars", spread_path[:2], spread_path[2:4], secret, filename_clean
    )

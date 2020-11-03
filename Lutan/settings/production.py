import os
from Lutan.settings.base import *

DEBUG = False
# must set settings.ALLOWED_HOSTS if DEBUG is False.

ALLOWED_HOST = os.getenv('ALLOWED_HOST', None)
if ALLOWED_HOST is not None:
    ALLOWED_HOSTS.append(ALLOWED_HOST)

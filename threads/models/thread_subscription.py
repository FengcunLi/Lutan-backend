from django.conf import settings
from django.db import models
from django.utils import timezone

from threads.models.thread import Thread


class ThreadSubscription(models.Model):
    subscriber = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   on_delete=models.CASCADE)
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE,
                               related_query_name='thread_subscription')
    time = models.DateTimeField(default=timezone.now)

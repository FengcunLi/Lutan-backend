from django.conf import settings
from django.db import models

from posts.models.post import Post


class PostReport(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    reporter = models.ForeignKey(settings.AUTH_USER_MODEL,
                                 on_delete=models.CASCADE)
    content = models.TextField()
    is_closed = models.BooleanField(default=False)
    closed_on = models.DateTimeField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)

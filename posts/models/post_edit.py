from django.conf import settings
from django.db import models

from posts.models.post import Post


class PostEdit(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    editor = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)

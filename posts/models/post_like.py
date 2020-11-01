from django.conf import settings
from django.db import models
from django.utils import timezone

from posts.models.post import Post


class PostLike(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='post_likes')
    liker = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE)
    time = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ['post', 'liker']

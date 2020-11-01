from os import error

from rest_framework import serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.validators import qs_exists

from permissions.post import (CanAddPostInThisThread,
                              CanDeletePostInThisThread, CanLikePostGlobally,
                              CanLikePostInThisThread, IsPoster)
from posts.models.post import Post
from posts.models.post_like import PostLike
from posts.serializers.post import (PostReadOnlySerializer,
                                    PostWritableSerializer)
from posts.serializers.post_like import PostLikeSerializer
from users.permissions import IsAdmin, IsGeneralUser


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()

    def get_serializer_class(self):
        if self.action in ["create", "partial_update", "update"]:
            return PostWritableSerializer
        elif self.action == 'like':
            return PostLikeSerializer
        else:
            return PostReadOnlySerializer

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [
                IsAuthenticated, IsAdmin | IsGeneralUser | CanAddPostInThisThread]
        elif self.action == 'destroy':
            self.permission_classes = [
                IsAuthenticated, IsAdmin | IsPoster | CanDeletePostInThisThread]
        elif self.action in ['like', 'cancel_like']:
            self.permission_classes = [
                IsAuthenticated, IsAdmin | IsGeneralUser | CanLikePostGlobally | CanLikePostInThisThread]
        return super().get_permissions()

    @action(
        methods=['POST'],
        detail=True,
    )
    def like(self, request, pk=None):
        # validate the post pk in url by calling get_object which inside will call
        # get_object_or_404
        post = self.get_object()

        if qs_exists(PostLike.objects.filter(post=post, liker=request.user)):
            raise serializers.ValidationError(
                'You already liked this post', code='unique')

        post_like = PostLike(post=post, liker=request.user)
        post_like.save()
        serializer = self.get_serializer(post_like)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(
        methods=['DELETE'],
        detail=True,
    )
    def cancel_like(self, request, pk=None):
        # validate the post pk in url by calling get_object which inside will call
        # get_object_or_404
        post = self.get_object()

        if not qs_exists(PostLike.objects.filter(post=post, liker=request.user)):
            raise serializers.ValidationError(
                'You can not cancel your like because you did not like this post before.')

        instance = PostLike.objects.get(post=post, liker=request.user)
        instance.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

from django.utils.html import escape
from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers
from rest_framework_recursive.fields import RecursiveField

from avatars.serializers import AvatarSerializer
from posts.models.post import Post
from posts.models.post_like import PostLike
from posts.serializers.post_like import PostLikeSerializer
from threads import models
from users.models import UserProxy
from users.permissions import is_group_member


class PosterSerializer(serializers.ModelSerializer):
    avatars = AvatarSerializer(many=True, read_only=True)

    class Meta:
        model = UserProxy
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True}
        }


class PostReadOnlySerializer(serializers.ModelSerializer):
    poster = PosterSerializer()
    children = serializers.ListSerializer(read_only=True,
                                          child=RecursiveField())
    post_likes = PostLikeSerializer(many=True, read_only=True)
    can_like_this_post = serializers.SerializerMethodField()
    liked_by_current_user = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = '__all__'

    @swagger_serializer_method(serializer_or_field=serializers.BooleanField)
    def get_can_like_this_post(self, post):
        user = self.context['request'].user
        return any([
            is_group_member(user, 'general_user'),
            user.has_perm('can_like_post_globally'),
            user.has_perm('can_like_post_in_this_thread', post.thread)
        ])

    @swagger_serializer_method(serializer_or_field=serializers.BooleanField)
    def get_liked_by_current_user(self, post):
        user = self.context['request'].user

        if not user.is_authenticated:
            return False
        return PostLike.objects.filter(post=post, liker=user).exists()


class PostWritableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

    def to_internal_value(self, data):
        data["content"] = escape(data["content"])
        return super().to_internal_value(data)

    def validate_poster(self, value):
        if self.context['request'].user.id != value.id:
            raise serializers.ValidationError(
                "The authenticated user and poster should be the same.")
        return value

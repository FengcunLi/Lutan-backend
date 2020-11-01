from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from posts.models import PostLike


class PostLikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = PostLike
        fields = '__all__'
        read_only_fields = ['post', 'liker']

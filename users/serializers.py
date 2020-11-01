import djoser
from rest_framework import serializers

from avatars.serializers import AvatarSerializer
from users.models import UserProxy


class UserSerializer(djoser.serializers.UserSerializer):
    avatars = AvatarSerializer(many=True, read_only=True)
    posts = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    threads = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    followers = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = UserProxy
        fields = '__all__'
        read_only_fields = (UserProxy.USERNAME_FIELD,)
        extra_kwargs = {
            'password': {'write_only': True}
        }

        # drf-yasg: a string which will be used as the model definition name for this serializer class;
        ref_name = 'UserProxy'

from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers

from avatars.serializers import AvatarSerializer
from categories.models import Category
from permissions.thread import IsStarter
from posts.serializers.post import PostReadOnlySerializer
from threads.models import Thread
from users.models import UserProxy
from users.permissions import is_group_member


class StarterSerializer(serializers.ModelSerializer):
    avatars = AvatarSerializer(many=True, read_only=True)

    class Meta:
        model = UserProxy
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True}
        }


class CategorySimpleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['id', 'name']


class PermissionsMixin(object):
    @swagger_serializer_method(serializer_or_field=serializers.BooleanField)
    def get_can_delete_this_thread(self, thread):
        user = self.context['request'].user
        return any([
            is_group_member(user, 'admin'),
            IsStarter().has_object_permission(
                self.context['request'], self.context['view'], thread),
            user.has_perm('can_delete_this_thread', thread)
        ])

    @swagger_serializer_method(serializer_or_field=serializers.BooleanField)
    def get_can_change_this_thread(self, thread):
        user = self.context['request'].user
        return any([
            is_group_member(user, 'admin'),
            IsStarter().has_object_permission(
                self.context['request'], self.context['view'], thread),
            user.has_perm('can_change_this_thread', thread)
        ])


class ThreadListSerializer(serializers.ModelSerializer, PermissionsMixin):
    starter = StarterSerializer(read_only=True)
    posts = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    category = CategorySimpleSerializer()
    last_activity = serializers.SerializerMethodField()
    can_delete_this_thread = serializers.SerializerMethodField()
    can_change_this_thread = serializers.SerializerMethodField()

    class Meta:
        model = Thread
        exclude = ['content', 'title_search_vector', 'content_search_vector']
        # drf-yasg: a string which will be used as the model definition name for this serializer class;
        ref_name = 'ThreadListModel'

    @swagger_serializer_method(serializer_or_field=serializers.DateTimeField)
    def get_last_activity(self, obj):
        return obj.latest


class ThreadRetrieveSerializer(serializers.ModelSerializer, PermissionsMixin):
    starter = StarterSerializer(read_only=True)
    posts = PostReadOnlySerializer(many=True, read_only=True)
    category = CategorySimpleSerializer()
    can_delete_this_thread = serializers.SerializerMethodField()
    can_change_this_thread = serializers.SerializerMethodField()

    class Meta:
        model = Thread
        exclude = ['title_search_vector', 'content_search_vector']
        # drf-yasg: a string which will be used as the model definition name for this serializer class;
        ref_name = 'ThreadRetrieveModel'


class ThreadWritableSerializer(serializers.ModelSerializer):
    starter = serializers.PrimaryKeyRelatedField(
        queryset=UserProxy.objects.all())

    class Meta:
        model = Thread
        exclude = ['title_search_vector', 'content_search_vector']

    def validate_starter(self, value):
        if self.context['request'].user.id != value.id:
            raise serializers.ValidationError(
                "The authenticated user and thread starter should be the same.")
        return value

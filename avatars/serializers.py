import os
from io import BytesIO

from django.conf import settings
from django.core.files.base import ContentFile
from PIL import Image
from rest_framework import serializers

from avatars.models import Avatar
from avatars.signals import resize_original_avatar


class AvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Avatar
        fields = '__all__'
        read_only_fields = ['user', 'width', 'height']

    def to_internal_value(self, value):
        image = Image.open(value['image'])

        # strip image of animation, convert to RGBA
        image.seek(0)
        image.copy().convert("RGBA")

        image_stream = BytesIO()
        image.save(image_stream, "PNG")
        new_file_name = os.path.splitext(value['image'].name)[0] + '.PNG'
        value['image'] = ContentFile(image_stream.getvalue(), new_file_name)

        return super().to_internal_value(value)

    def create(self, validated_data):
        user = self.context['request'].user
        if not user.is_authenticated:
            raise serializers.ValidationError('user is not authenticated')

        # clear existing avatars before create new one
        existing_avatars = Avatar.objects.filter(user=user)
        for avatar in existing_avatars:
            avatar.image.delete()
        existing_avatars.delete()

        validated_data['original'] = True
        validated_data['user'] = user
        original_avatar = super().create(validated_data)
        resize_original_avatar.send(None, original_avatar=original_avatar)
        return original_avatar

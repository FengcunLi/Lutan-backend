from io import BytesIO

from django.apps import AppConfig, apps
from django.conf import settings
from django.core.files.base import ContentFile
from django.db.models.signals import post_save
from PIL import Image

from avatars.signals import resize_original_avatar
from avatars.utils import generate_default_avatar


def resize_original_avatar_receiver(sender, **kwargs):
    Avatar = apps.get_model(app_label='avatars', model_name='Avatar')

    original = kwargs["original_avatar"]
    original_image = Image.open(original.image.path)
    user = original.user

    for size in settings.AVATARS_SIZES:
        image_stream = BytesIO()
        image = original_image.resize((size, size), Image.ANTIALIAS)
        image.save(image_stream, "PNG")

        Avatar.objects.create(
            user=user,
            image=ContentFile(image_stream.getvalue(),
                              name='dummy_name_otherwise_create_will_work_improperly_silently'),
            original=False
        )


def default_avatar(sender, **kwargs):
    Avatar = apps.get_model(app_label='avatars', model_name='Avatar')

    instance = kwargs['instance']
    if kwargs['created'] and len(instance.first_name) > 0:
        image = generate_default_avatar(instance.first_name[0])
        image_stream = BytesIO()
        image.save(image_stream, "PNG")

        original_avatar = Avatar.objects.create(
            user=instance,
            image=ContentFile(image_stream.getvalue(),
                              name='dummy_name_otherwise_create_will_work_improperly_silently'),
            original=True
        )
        resize_original_avatar.send(None, original_avatar=original_avatar)


class AvatarsConfig(AppConfig):
    name = 'avatars'

    def ready(self):
        resize_original_avatar.connect(resize_original_avatar_receiver)
        post_save.connect(default_avatar,
                          sender=settings.AUTH_USER_MODEL)

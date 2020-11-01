from django.apps import AppConfig, apps
from django.conf import settings
from django.db.models.signals import post_save


def add_to_default_group(sender, **kwargs):
    Group = apps.get_model(app_label='auth', model_name='Group')

    user = kwargs["instance"]
    if kwargs["created"]:
        group = Group.objects.get(name='general_user')
        user.groups.add(group)


class UsersConfig(AppConfig):
    name = 'users'

    def ready(self):
        post_save.connect(add_to_default_group,
                          sender=settings.AUTH_USER_MODEL)

import hashlib
import random

from django.conf import settings
from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand, CommandParser
from django.db.models import QuerySet
from faker import Factory, Generator
from tqdm import tqdm

from users.models import User


class Command(BaseCommand):
    help = 'Creates fake users.'

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            'users',
            help='number of users to create',
            nargs='?',
            type=int,
            default=10
        )

    def handle(self, *args, **options):
        number_to_create: int = options['users']
        fake: Generator = Factory.create(
            getattr(settings, 'FAKER_LOCALE', None))
        queryset: QuerySet = User.objects.all()
        existing_emails = set(queryset.values_list('email', flat=True))
        groups: QuerySet = Group.objects.all()

        new_user_first_last_names = []
        while number_to_create > 0:
            first_name, last_name = fake.first_name(), fake.last_name()
            email = f'{first_name}.{last_name}@gmail.com'
            if email not in existing_emails:
                new_user_first_last_names.append((first_name, last_name))
                existing_emails.add(email)
                number_to_create -= 1

        for first_name, last_name in tqdm(new_user_first_last_names, desc='Creating new users'):
            email = f'{first_name}.{last_name}@gmail.com'
            is_superuser = random.choices(
                [True, False], weights=[0.1, 0.9])[0]
            user: User = User.objects.create_user(
                email=email,
                password='password',
                first_name=first_name,
                last_name=last_name,
                is_superuser=is_superuser,
                is_staff=is_superuser or (random.choices(
                    [True, False], weights=[0.1, 0.9])[0]),
                is_active=random.choices(
                    [True, False], weights=[0.9, 0.1])[0],
            )
            group_number = random.randint(0, groups.count())
            # NOTE: random.choices: Return a k sized list of population elements chosen with **replacement**.
            user.groups.set(set(random.choices(groups, k=group_number)))
            number_to_create -= 1

    # @staticmethod
    # def get_fake_avatars(email):
    #     GRAVATAR_URL = "https://www.gravatar.com/avatar/%s?s=%s&d=retro"
    #     AVATAR_SIZES = (400, 200, 100)

    #     email_hash = hashlib.md5(
    #         email.lower().encode("utf-8")).hexdigest()
    #     return [{"size": size, "url": GRAVATAR_URL % (email_hash, size)} for size in AVATAR_SIZES]

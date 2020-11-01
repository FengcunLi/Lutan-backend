from django.conf import settings
from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand, CommandParser
from faker import Factory, Generator
from tqdm import tqdm


class Command(BaseCommand):
    help = 'Creates fake groups using faker.Generator.company.'

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            'groups',
            help='number of groups to create',
            nargs='?',
            type=int,
            default=10
        )

    def handle(self, *args, **options):
        number_to_create: int = options['groups']
        fake: Generator = Factory.create(
            getattr(settings, 'FAKER_LOCALE', None))

        existing_names = set(
            Group.objects.all().values_list('name', flat=True))
        new_names = []
        while number_to_create > 0:
            name = fake.company()
            if name not in existing_names:
                new_names.append(name)
                existing_names.add(name)
            number_to_create -= 1

        for name in tqdm(new_names, desc='Creating new groups'):
            Group.objects.create(name=name)

import random

from django.conf import settings
from django.core.management.base import BaseCommand, CommandParser
from django.db.models import QuerySet
from faker import Factory, Generator
from tqdm import tqdm

from categories.models import Category


class Command(BaseCommand):
    help = 'Creates fake categories using faker.Generator.street_name.'

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            'categories',
            help='number of categories to create',
            nargs='?',
            type=int,
            default=10
        )

    def handle(self, *args, **options):
        number_to_create: int = options['categories']
        fake: Generator = Factory.create(
            getattr(settings, 'FAKER_LOCALE', None))
        categories: QuerySet = Category.objects.all()
        assert categories.exists() == True, 'At least one root category should exist.'

        existing_names = set(categories.values_list('name', flat=True))
        new_names = []
        while number_to_create > 0:
            name = fake.street_name()
            if name not in existing_names:
                new_names.append(name)
                existing_names.add(name)
                number_to_create -= 1

        for new_name in tqdm(new_names, desc='Creating new categories'):
            parent: Category = random.choice(categories)
            new_category: Category = Category(
                name=new_name,
                description=fake.paragraph(),
                is_closed=random.choices(
                    [True, False], weights=[0.1, 0.9])[0],
                require_threads_approval=random.choices(
                    [True, False], weights=[0.1, 0.9])[0],
                require_posts_approval=random.choices(
                    [True, False], weights=[0.1, 0.9])[0]
            )
            new_category.insert_at(parent, position='last-child', save=True)
            # Refresh categories from database
            categories = categories.all()

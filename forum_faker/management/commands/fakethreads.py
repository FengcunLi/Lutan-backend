import random
from datetime import datetime
from typing import List

from django.conf import settings
from django.core.management.base import BaseCommand, CommandParser
from django.db.models.expressions import F
from django.utils.timezone import make_aware
from faker import Factory, Generator
from tqdm import tqdm

from categories.models import Category
from threads.models import Thread
from users.models import User

UNSPLASH_URL = 'http://unsplash.it/%d/%d?random&gravity=center'


class Command(BaseCommand):
    help = 'Creates fake threads.'

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            'threads',
            help='number of threads to create',
            nargs='?',
            type=int,
            default=100
        )

    def handle(self, *args, **options):
        number_to_create: int = options['threads']
        fake: Generator = Factory.create(
            getattr(settings, 'FAKER_LOCALE', None))
        users = User.objects.all()
        categories = Category.objects.filter(lft=F('rght')-1)

        for _ in tqdm(range(number_to_create), desc='Creating new threads'):
            title: str = fake.sentence(nb_words=20)
            weight: int = random.choices(
                [Thread.WEIGHT_DEFAULT, Thread.WEIGHT_PINNED_LOCALLY,
                    Thread.WEIGHT_PINNED_GLOBALLY],
                weights=[0.85, 0.1, 0.05])[0]
            is_unapproved: bool = random.choices([True, False],
                                                 weights=[0.1, 0.9])[0]
            is_hidden: bool = random.choices([True, False],
                                             weights=[0.1, 0.9])[0]
            is_closed: bool = random.choices([True, False],
                                             weights=[0.1, 0.9])[0]

            category: Category = random.choice(categories)
            starter: User = random.choice(users)
            created_on: datetime = make_aware(
                fake.date_time_this_decade(
                    before_now=True, after_now=False, tzinfo=None)
            )

            paragraphs: List[str] = []
            for _ in range(random.randint(1, 20)):
                if random.random() < 0.1:
                    width = random.randint(100, 1600)
                    height = random.randint(100, 1600)
                    url = UNSPLASH_URL % (width, height)
                    paragraphs.append(
                        f'<p><img src="{url}" alt="" /></p>')
                else:
                    sentences = fake.sentences(random.randint(1, 20))
                    paragraph = ' '.join(sentences)
                    paragraphs.append(f'<p>{paragraph}</p>')

            content = ''.join(paragraphs)

            Thread(
                title=title,
                content=content,
                weight=weight,
                is_unapproved=is_unapproved,
                is_hidden=is_hidden,
                is_closed=is_closed,
                category=category,
                starter=starter,
                created_on=created_on
            ).save()

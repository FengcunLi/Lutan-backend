import random
from datetime import datetime
from typing import List, Union

from django.conf import settings
from django.core.management.base import BaseCommand, CommandParser
from django.utils.timezone import make_aware
from faker import Factory, Generator
from tqdm import tqdm

from posts.models import Post
from threads.models import Thread
from users.models import User

UNSPLASH_URL = 'http://unsplash.it/%d/%d?random&gravity=center'


class Command(BaseCommand):
    help = 'Creates fake posts.'

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            'posts',
            help='number of posts to create',
            nargs='?',
            type=int,
            default=100
        )

    def handle(self, *args, **options):
        number_to_create: int = options['posts']
        fake: Generator = Factory.create(
            getattr(settings, 'FAKER_LOCALE', None))
        users = User.objects.all()
        threads = Thread.objects.prefetch_related('posts').all()

        for _ in tqdm(range(number_to_create), desc='Creating new posts'):
            thread: Thread = random.choice(threads)

            # This New post is going to be the reply for parent
            existing_posts: List[Union[Post, None]] = list(thread.posts.all())
            existing_posts.append(None)
            parent = random.choice(existing_posts)

            poster: User = random.choice(users)

            is_unapproved: bool = random.choices([True, False],
                                                 weights=[0.1, 0.9])[0]
            is_hidden: bool = random.choices([True, False],
                                             weights=[0.1, 0.9])[0]

            datetime_start = thread.created_on
            if parent is not None:
                assert parent.created_on == thread.created_on or parent.created_on > thread.created_on, \
                    'Post should be posted after the creation of thread.'
                datetime_start = parent.created_on

            created_on: datetime = make_aware(
                fake.date_time_between_dates(datetime_start=datetime_start,
                                             datetime_end=None, tzinfo=None)
            )

            parsed_paragraphs: List[str] = []
            for _ in range(random.randint(1, 5)):
                if random.random() < 0.1:
                    width = random.randint(100, 1600)
                    height = random.randint(100, 1600)
                    url = UNSPLASH_URL % (width, height)
                    parsed_paragraphs.append(
                        f'<p><img src="{url}" alt="" /></p>')
                else:
                    sentences = fake.sentences(random.randint(1, 10))
                    raw_paragraph = ' '.join(sentences)
                    parsed_paragraph = f'<p>{raw_paragraph}</p>'
                    parsed_paragraphs.append(parsed_paragraph)

            content = '\n'.join(parsed_paragraphs)

            Post(
                parent=parent,
                thread=thread,
                poster=poster,
                content=content,
                is_unapproved=is_unapproved,
                is_hidden=is_hidden,
                created_on=created_on
            ).save()

            # Refresh threads from database in order to refresh thread's posts
            threads = Thread.objects.prefetch_related('posts').all()

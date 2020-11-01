import random
from datetime import datetime

from django.conf import settings
from django.core.management.base import BaseCommand, CommandParser
from django.utils.timezone import make_aware
from faker import Factory, Generator
from tqdm import tqdm

from posts.models import Post, PostLike
from users.models import User


class Command(BaseCommand):
    help = 'Creates fake post likes.'

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            'postlikes',
            help='number of post likes to create',
            nargs='?',
            type=int,
            default=1000
        )

    def handle(self, *args, **options):
        number_to_create: int = options['postlikes']
        fake: Generator = Factory.create(
            getattr(settings, 'FAKER_LOCALE', None))
        users = User.objects.all()
        posts = Post.objects.all()

        for _ in tqdm(range(number_to_create), desc='Creating new post likes'):
            post: Post = random.choice(posts)
            liker: User = random.choice(users)
            if not PostLike.objects.filter(post=post, liker=liker).exists():
                datetime_start = post.created_on

                created_on: datetime = make_aware(
                    fake.date_time_between_dates(datetime_start=datetime_start,
                                                 datetime_end=None, tzinfo=None)
                )

                PostLike(
                    post=post,
                    liker=liker,
                    time=created_on
                ).save()

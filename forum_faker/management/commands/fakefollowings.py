import random

from django.core.management.base import BaseCommand, CommandParser
from django.db.models import QuerySet
from tqdm import tqdm

from users.models import User


class Command(BaseCommand):
    help = 'Creates fake followings.'

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            'followings',
            help='number of followings to create',
            nargs='?',
            type=int,
            default=100
        )

    def handle(self, *args, **options):
        number_to_create: int = options['followings']
        queryset: QuerySet = User.objects.all()
        users = list(queryset)

        for _ in tqdm(range(number_to_create), desc='Creating new followings'):
            # NOTE: random.choices: Return a k sized list of population elements chosen with **replacement**.
            user_1, user_2 = random.choices(users, k=2)
            if (user_1.id != user_2.id):
                user_1.followings.add(user_2)

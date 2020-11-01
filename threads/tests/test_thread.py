import random

import pytest
from pytest import fixture

from categories.tests.test_tree import category_tree, root
from threads.models.thread import Thread
from users.tests.test_djoser import users

pytestmark = pytest.mark.django_db()


def fake_thread(faker, users, categories):
    data = {
        'title': faker.sentence(),
        'original_content': faker.text(),
        'weight': random.choice([Thread.WEIGHT_DEFAULT, Thread.WEIGHT_PINNED_LOCALLY, Thread.WEIGHT_PINNED_LOCALLY]),
        'is_unapproved': random.choices([True, False], weights=[0.1, 0.9], k=1)[0],
        'is_hidden': random.choices([True, False], weights=[0.1, 0.9], k=1)[0],
        'is_closed': random.choices([True, False], weights=[0.1, 0.9], k=1)[0],
        'category': random.choice([c for c in categories if c['is_leaf_node']])['id'],
        'starter': random.choice(users)['id'],
    }
    return data


def test_create_thread(client, faker, users, category_tree):
    response = client.get('/categories/')
    assert response.status_code == 200
    categories = response.data
    data = fake_thread(faker, users, categories)
    response = client.post('/categories/%s/threads/' % data['category'], data)
    assert response.status_code == 201


@fixture
def threads(client, faker, users, category_tree):
    num = 1000
    for i in range(num):
        test_create_thread(client, faker, users, category_tree)
    response = client.get('/categories/1/threads/')
    assert response.status_code == 200
    assert len(response.data) == num


def test_list_create(threads):
    pass


def test_my(threads):
    pass

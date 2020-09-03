import pytest
from mixer.backend.django import mixer
from pytest import fixture
from rest_framework.test import APIClient

from categories import PUBLIC_THREADS_CATEGORY_TREE_ROOT_NAME
from categories.models import Category

pytestmark = pytest.mark.django_db()


@fixture
def client():
    return APIClient()


@fixture
def root():
    root = Category.objects.create(
        name=PUBLIC_THREADS_CATEGORY_TREE_ROOT_NAME,
        level=0,
    )
    return {
        'id': root.id,
        'lft': root.lft,
        'rght': root.rght
    }


def create(client, parent, faker):
    data = {
        'name': faker.catch_phrase().title(),
        'description': faker.catch_phrase(),
        'parent': parent['id'],
    }
    response_1 = client.post('/categories/', data)
    assert response_1.status_code == 201

    response_2 = client.get('/categories/%s/' % parent['id'])
    assert response_2.status_code == 200

    child = response_1.data
    refreshed_parent = response_2.data
    assert refreshed_parent['lft'] < child['lft'] < child['rght'] < refreshed_parent['rght']
    return child


def test_create(client, root, faker):
    c_1 = create(client, root, faker)
    c_2 = create(client, root, faker)
    c_3 = create(client, root, faker)
    c_4 = create(client, c_2, faker)

    response = client.get('/categories/1/tree/')
    tree = response.data
    assert response.status_code == 200
    assert len(tree['subcategories']) == 3
    assert len(tree['subcategories'][0]['subcategories']) == 0
    assert len(tree['subcategories'][1]['subcategories']) == 1
    assert len(tree['subcategories'][2]['subcategories']) == 0

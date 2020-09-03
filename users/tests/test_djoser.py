import pytest
from django.conf import settings
from mixer.backend.django import mixer
from pytest import fixture
from rest_framework.test import APIClient

pytestmark = pytest.mark.django_db()


@fixture
def client():
    return APIClient()


@fixture
def user_data(faker):
    return {'username': faker.name().replace(' ', ''),
            'password': faker.password(),
            'email': faker.email()}


@fixture
def user():
    return mixer.blend(settings.AUTH_USER_MODEL)


def test_create_user(client, user_data):
    response = client.post('/auth/users/', user_data)

    assert response.status_code == 201


def test_obtain_auth_token(client, user_data):
    test_create_user(client, user_data)
    data = {'email': user_data['email'],
            'password': user_data['password']}
    response = client.post(
        '/auth/token/login/', data)

    assert response.status_code == 200
    assert 'auth_token' in response.data

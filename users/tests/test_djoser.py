import pytest
from django.conf import settings
from mixer.backend.django import mixer
from pytest import fixture

pytestmark = pytest.mark.django_db()


def get_user_data(faker):
    return {'username': faker.name().replace(' ', ''),
            'password': faker.password(),
            'email': faker.email()}


@fixture
def user_data(faker):
    return get_user_data(faker)


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


@fixture
def users(client, faker):
    users_list = []
    num = 100
    for i in range(num):
        from faker.providers.person.en import Provider
    first_names = Provider.first_names[:num]
    last_names = Provider.last_names[:num]
    Provider.
    for i in range(num):
    response = client.post('/auth/users/', get_user_data(faker))
    assert response.status_code == 201
    users_list.append(response.data)
    return users_list

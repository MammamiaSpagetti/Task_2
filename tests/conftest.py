import pytest
import requests

from data import REQUEST_TIMEOUT
from helpers import generate_user_data
from urls import INGREDIENTS_URL, LOGIN_USER_URL, REGISTER_USER_URL, USER_URL


def delete_user(access_token):
    response = requests.delete(
        USER_URL,
        headers={'Authorization': access_token},
        timeout=REQUEST_TIMEOUT,
    )
    if response.status_code not in (200, 202):
        pytest.fail(
            f'Не удалось удалить тестового пользователя: '
            f'{response.status_code} {response.text}'
        )


@pytest.fixture
def new_user_context():
    context = {
        'data': generate_user_data(),
        'access_token': None,
    }

    yield context

    access_token = context['access_token']
    if access_token is None:
        login_response = requests.post(
            LOGIN_USER_URL,
            json={
                'email': context['data']['email'],
                'password': context['data']['password'],
            },
            timeout=REQUEST_TIMEOUT,
        )
        if login_response.status_code == 200:
            access_token = login_response.json()['accessToken']

    if access_token is not None:
        delete_user(access_token)


@pytest.fixture
def registered_user():
    user_data = generate_user_data()
    response = requests.post(
        REGISTER_USER_URL,
        json=user_data,
        timeout=REQUEST_TIMEOUT,
    )
    if response.status_code != 200:
        pytest.fail(
            f'Не удалось создать тестового пользователя: '
            f'{response.status_code} {response.text}'
        )

    access_token = response.json()['accessToken']
    user = {
        'data': user_data,
        'access_token': access_token,
    }

    yield user

    delete_user(access_token)


@pytest.fixture(scope='session')
def ingredient_ids():
    response = requests.get(INGREDIENTS_URL, timeout=REQUEST_TIMEOUT)
    if response.status_code != 200:
        pytest.fail(
            f'Не удалось получить ингредиенты: '
            f'{response.status_code} {response.text}'
        )

    ingredients = response.json()['data']
    if len(ingredients) < 2:
        pytest.fail('Сервис вернул меньше двух ингредиентов')

    return [ingredients[0]['_id'], ingredients[1]['_id']]

import allure
import requests

from data import (
    INGREDIENTS_REQUIRED_MESSAGE,
    INVALID_INGREDIENT_HASH,
    REQUEST_TIMEOUT,
)
from helpers import attach_response
from urls import ORDERS_URL


@allure.feature('Создание заказа')
class TestCreateOrder:
    @allure.title('Создание заказа с авторизацией и ингредиентами')
    def test_create_order_with_authorization_returns_order(
        self, registered_user, ingredient_ids
    ):
        response = requests.post(
            ORDERS_URL,
            headers={'Authorization': registered_user['access_token']},
            json={'ingredients': ingredient_ids},
            timeout=REQUEST_TIMEOUT,
        )
        attach_response(response)
        response_body = response.json()

        assert response.status_code == 200
        assert response_body['success'] is True
        assert isinstance(response_body['order']['number'], int)

    @allure.title('Создание заказа без авторизации с ингредиентами')
    def test_create_order_without_authorization_returns_order(self, ingredient_ids):
        response = requests.post(
            ORDERS_URL,
            json={'ingredients': ingredient_ids},
            timeout=REQUEST_TIMEOUT,
        )
        attach_response(response)
        response_body = response.json()

        assert response.status_code == 200
        assert response_body['success'] is True
        assert isinstance(response_body['order']['number'], int)

    @allure.title('Создание заказа без ингредиентов')
    def test_create_order_without_ingredients_returns_error(self, registered_user):
        response = requests.post(
            ORDERS_URL,
            headers={'Authorization': registered_user['access_token']},
            json={'ingredients': []},
            timeout=REQUEST_TIMEOUT,
        )
        attach_response(response)

        assert response.status_code == 400
        assert response.json() == {
            'success': False,
            'message': INGREDIENTS_REQUIRED_MESSAGE,
        }

    @allure.title('Создание заказа с неверным хешем ингредиента')
    def test_create_order_with_invalid_ingredient_hash_returns_server_error(
        self, registered_user
    ):
        response = requests.post(
            ORDERS_URL,
            headers={'Authorization': registered_user['access_token']},
            json={'ingredients': [INVALID_INGREDIENT_HASH]},
            timeout=REQUEST_TIMEOUT,
        )
        attach_response(response)

        assert response.status_code == 500
        assert 'Internal Server Error' in response.text

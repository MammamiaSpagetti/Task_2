import allure
import requests

from data import REQUEST_TIMEOUT, UNAUTHORIZED_MESSAGE
from helpers import attach_response
from urls import ORDERS_URL


@allure.feature('Получение заказов пользователя')
class TestGetUserOrders:
    @allure.title('Получение заказов авторизованного пользователя')
    def test_get_authorized_user_orders_returns_created_order(
        self, registered_user, ingredient_ids
    ):
        create_response = requests.post(
            ORDERS_URL,
            headers={'Authorization': registered_user['access_token']},
            json={'ingredients': ingredient_ids},
            timeout=REQUEST_TIMEOUT,
        )
        attach_response(create_response)
        created_order_number = create_response.json()['order']['number']

        response = requests.get(
            ORDERS_URL,
            headers={'Authorization': registered_user['access_token']},
            timeout=REQUEST_TIMEOUT,
        )
        attach_response(response)
        response_body = response.json()

        assert create_response.status_code == 200
        assert create_response.json()['success'] is True
        assert response.status_code == 200
        assert response_body['success'] is True
        assert any(
            order['number'] == created_order_number for order in response_body['orders']
        )

    @allure.title('Получение заказов без авторизации')
    def test_get_unauthorized_user_orders_returns_error(self):
        response = requests.get(ORDERS_URL, timeout=REQUEST_TIMEOUT)
        attach_response(response)

        assert response.status_code == 401
        assert response.json() == {
            'success': False,
            'message': UNAUTHORIZED_MESSAGE,
        }

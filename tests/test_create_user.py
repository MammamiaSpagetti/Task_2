import allure
import pytest
import requests

from data import (
    REQUEST_TIMEOUT,
    REQUIRED_FIELDS_MESSAGE,
    USER_ALREADY_EXISTS_MESSAGE,
)
from helpers import attach_response
from urls import REGISTER_USER_URL


@allure.feature('Создание пользователя')
class TestCreateUser:
    @allure.title('Создание уникального пользователя')
    def test_create_unique_user_returns_success(self, new_user_context):
        response = requests.post(
            REGISTER_USER_URL,
            json=new_user_context['data'],
            timeout=REQUEST_TIMEOUT,
        )
        attach_response(response)
        response_body = response.json()
        if response.status_code == 200:
            new_user_context['access_token'] = response_body.get('accessToken')

        assert response.status_code == 200
        assert response_body['success'] is True
        assert response_body['user'] == {
            'email': new_user_context['data']['email'],
            'name': new_user_context['data']['name'],
        }

    @allure.title('Повторное создание зарегистрированного пользователя')
    def test_create_existing_user_returns_error(self, registered_user):
        response = requests.post(
            REGISTER_USER_URL,
            json=registered_user['data'],
            timeout=REQUEST_TIMEOUT,
        )
        attach_response(response)

        assert response.status_code == 403
        assert response.json() == {
            'success': False,
            'message': USER_ALREADY_EXISTS_MESSAGE,
        }

    @allure.title('Создание пользователя без обязательного поля: {missing_field}')
    @pytest.mark.parametrize('missing_field', ['email', 'password', 'name'])
    def test_create_user_without_required_field_returns_error(
        self, new_user_context, missing_field
    ):
        request_body = new_user_context['data'].copy()
        request_body.pop(missing_field)

        response = requests.post(
            REGISTER_USER_URL,
            json=request_body,
            timeout=REQUEST_TIMEOUT,
        )
        attach_response(response)

        assert response.status_code == 403
        assert response.json() == {
            'success': False,
            'message': REQUIRED_FIELDS_MESSAGE,
        }

from uuid import uuid4

import allure
import pytest
import requests

from data import REQUEST_TIMEOUT, UNAUTHORIZED_MESSAGE
from helpers import attach_response
from urls import LOGIN_USER_URL, USER_URL


@allure.feature('Изменение данных пользователя')
class TestUpdateUser:
    @allure.title('Изменение поля авторизованного пользователя: {field}')
    @pytest.mark.parametrize('field', ['email', 'name', 'password'])
    def test_update_authorized_user_field_returns_updated_data(
        self, registered_user, field
    ):
        unique_id = uuid4().hex
        new_values = {
            'email': f'updated_{unique_id}@example.com',
            'name': f'Updated_{unique_id[:8]}',
            'password': f'UpdatedPassword_{unique_id}',
        }
        new_value = new_values[field]

        response = requests.patch(
            USER_URL,
            headers={'Authorization': registered_user['access_token']},
            json={field: new_value},
            timeout=REQUEST_TIMEOUT,
        )
        attach_response(response)
        response_body = response.json()

        assert response.status_code == 200
        assert response_body['success'] is True

        if field == 'password':
            login_response = requests.post(
                LOGIN_USER_URL,
                json={
                    'email': registered_user['data']['email'],
                    'password': new_value,
                },
                timeout=REQUEST_TIMEOUT,
            )
            attach_response(login_response)
            assert login_response.status_code == 200
            assert login_response.json()['success'] is True
        else:
            assert response_body['user'][field] == new_value

    @allure.title('Изменение поля без авторизации: {field}')
    @pytest.mark.parametrize('field', ['email', 'name', 'password'])
    def test_update_unauthorized_user_field_returns_error(self, field):
        unique_id = uuid4().hex
        field_values = {
            'email': f'unauthorized_{unique_id}@example.com',
            'name': f'Unauthorized_{unique_id[:8]}',
            'password': f'UnauthorizedPassword_{unique_id}',
        }

        response = requests.patch(
            USER_URL,
            json={field: field_values[field]},
            timeout=REQUEST_TIMEOUT,
        )
        attach_response(response)

        assert response.status_code == 401
        assert response.json() == {
            'success': False,
            'message': UNAUTHORIZED_MESSAGE,
        }

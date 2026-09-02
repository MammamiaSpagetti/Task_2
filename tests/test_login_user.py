import allure
import requests

from data import INVALID_CREDENTIALS_MESSAGE, REQUEST_TIMEOUT
from helpers import attach_response, generate_user_data
from urls import LOGIN_USER_URL


@allure.feature('Авторизация пользователя')
class TestLoginUser:
    @allure.title('Авторизация существующего пользователя')
    def test_login_existing_user_returns_user_and_tokens(self, registered_user):
        response = requests.post(
            LOGIN_USER_URL,
            json={
                'email': registered_user['data']['email'],
                'password': registered_user['data']['password'],
            },
            timeout=REQUEST_TIMEOUT,
        )
        attach_response(response)
        response_body = response.json()

        assert response.status_code == 200
        assert response_body['success'] is True
        assert response_body['user'] == {
            'email': registered_user['data']['email'],
            'name': registered_user['data']['name'],
        }
        assert response_body['accessToken'].startswith('Bearer ')
        assert response_body['refreshToken']

    @allure.title('Авторизация с неверными почтой и паролем')
    def test_login_with_invalid_credentials_returns_error(self):
        invalid_user = generate_user_data()

        response = requests.post(
            LOGIN_USER_URL,
            json={
                'email': invalid_user['email'],
                'password': f"wrong_{invalid_user['password']}",
            },
            timeout=REQUEST_TIMEOUT,
        )
        attach_response(response)

        assert response.status_code == 401
        assert response.json() == {
            'success': False,
            'message': INVALID_CREDENTIALS_MESSAGE,
        }

from uuid import uuid4

import allure


def generate_user_data():
    unique_id = uuid4().hex
    return {
        'email': f'stellar_{unique_id}@example.com',
        'password': f'Password_{unique_id}',
        'name': f'User_{unique_id[:8]}',
    }


def attach_response(response):
    response_details = f'Status: {response.status_code}\nBody: {response.text}'
    allure.attach(
        response_details,
        name='API response',
        attachment_type=allure.attachment_type.TEXT,
    )

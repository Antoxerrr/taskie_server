import pytest
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

from taskie.api.users.logic.auth import Authenticator
from taskie.tests.base import TestClass
from taskie.tests.users.factory import TokenFactory, UserFactory


User = get_user_model()


@pytest.mark.django_db
class TestAuthenticator(TestClass):
    """Тесты для класса Authenticator."""

    tested_class = Authenticator

    def test_logout_do_delete_token(self):
        """Тест - логаут удаляет токен из базы."""
        token = TokenFactory()
        self.tested_class.logout(token.key)
        token_exists = Token.objects.filter(key=token.key).exists()
        assert not token_exists

    @staticmethod
    def _create_user(username, password):
        """Создание тестового пользователя."""
        user = UserFactory(
            username=username,
            email='test@test.test'
        )
        user.set_password(password)
        user.save()
        return user

    @staticmethod
    def _make_login_request(client, username, password):
        """Отправка запроса на авторизацию."""
        url = '/api/v1/users/auth/base/login/'
        data = {'username': username, 'password': password}
        return client.post(url, data)

    def test_login_success(self, client):
        """Тест успешной авторизации."""
        username = 'Valera'
        password = 'Valera228'
        self._create_user(username, password)

        response = self._make_login_request(client, username, password)

        assert response.status_code == 200
        assert 'user' in response.data
        assert 'token' in response.data

        user = response.data['user']
        assert user['username'] == username

    def test_login_failed(self, client):
        """Тест неудачной авторизации."""
        response = self._make_login_request(client, 'kek_lol', 'kek_lol')

        assert response.status_code == 400
        assert response.data['message'] == self.tested_class.WRONG_CREDENTIALS
        assert response.data['is_field_error'] is False

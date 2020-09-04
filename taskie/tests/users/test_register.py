import pytest
from django.contrib.auth import get_user_model

from taskie.api.exceptions import ValidationError
from taskie.api.users.logic.register import Registerer
from taskie.api.users.logic.validation import UserDataValidator
from taskie.tests.base import TestClass
from taskie.tests.users.factory import UserFactory

User = get_user_model()


@pytest.mark.django_db
class TestRegisterer(TestClass):
    """Тесты для класса Registerer."""

    tested_class = Registerer
    test_username = 'Valera'
    test_email = 'valera@valera.ru'

    def test_registration_success(self):
        """Тест удачной регистрации."""
        user_data = {
            'username': 'Valera',
            'password': 'Valera228',
            'password_confirmation': 'Valera228',
            'email': 'valera@valera.ru'
        }
        self.tested_class.register(user_data)

        # password_confirmation должен дропаться при регистрации,
        # password дропаем тут.
        user_data.pop('password')
        User.objects.get(**user_data)

    def _create_user(self):
        """Создание тестового пользователя."""
        user = UserFactory(
            username=self.test_username,
            email=self.test_email
        )
        return user

    def test_registration_failed(self):
        """Тест неудачной регистрации."""
        user_data = {
            'username': self.test_username,
            'password': 'Valera228',
            'password_confirmation': 'Valera2289',
            'email': self.test_email
        }

        # Сценарий - неверное подтверждение пароля
        with pytest.raises(ValidationError) as exc_info:
            self.tested_class.register(user_data)
        message, field = exc_info.value.args
        assert (
            message == UserDataValidator.WRONG_PASSWORD_CONFIRMATION
        )
        assert field == 'password'
        assert exc_info.value.detail['is_field_error'] is True

        # Сценарий - не уникальное имя пользователя
        self._create_user()
        user_data['password_confirmation'] = 'Valera228'
        with pytest.raises(ValidationError) as exc_info:
            self.tested_class.register(user_data)
        message, field = exc_info.value.args
        assert message == UserDataValidator.USERNAME_EXISTS
        assert field == 'username'
        assert exc_info.value.detail['is_field_error'] is True

        # Сценарий - не уникальный email
        user_data['username'] = 'somesuperuniqueusername'
        with pytest.raises(ValidationError) as exc_info:
            self.tested_class.register(user_data)
        message, field = exc_info.value.args
        assert message == UserDataValidator.EMAIL_EXISTS
        assert field == 'email'
        assert exc_info.value.detail['is_field_error'] is True

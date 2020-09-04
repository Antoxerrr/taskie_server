import pytest

from taskie.api.exceptions import ValidationError
from taskie.api.users.logic.validation import UserDataValidator
from taskie.tests.base import TestClass
from taskie.tests.users.factory import UserFactory

TEST_USERNAME = 'test'
TEST_EMAIL = 'test@test.test'


@pytest.mark.django_db
class TestUserDataValidator(TestClass):
    """Тестирование класса UserDataValidator."""

    tested_class = UserDataValidator

    def test_valid_password_confirmation(self):
        """Тест - одинаковые пароли не должны вызывать исключение."""
        assert self.tested_class.compare_passwords('asd', 'asd') is None

    def test_invalid_password_confirmation(self):
        """Тест - разные пароли должны вызывать ValidationError."""
        with pytest.raises(ValidationError):
            self.tested_class.compare_passwords('asd', 'asdasd')

    def test_username_is_unique(self):
        """Тест - имя пользователя уникально."""
        assert (
            self.tested_class.validate_username('someuniqueusername') is None
        )

    def test_username_is_not_unique(self):
        """Тест - имя пользователя НЕ уникально, вызовет ValidationError."""
        UserFactory(username=TEST_USERNAME, email=TEST_EMAIL)
        with pytest.raises(ValidationError):
            self.tested_class.validate_username(TEST_USERNAME)

    def test_email_is_unique(self):
        """Тест - email уникален."""
        assert self.tested_class.validate_email('someuniqueemail') is None

    def test_email_is_not_unique(self):
        """Тест - email НЕ уникален, вызовет ValidationError."""
        UserFactory(username=TEST_USERNAME, email=TEST_EMAIL)
        with pytest.raises(ValidationError):
            self.tested_class.validate_email(TEST_EMAIL)

from django.contrib.auth import get_user_model

from taskie.api.exceptions import ValidationError

User = get_user_model()


class UserDataValidator:
    """Валидатор пользовательских данных."""

    WRONG_PASSWORD_CONFIRMATION = 'Пароли не совпадают.'
    USERNAME_EXISTS = 'Имя пользователя уже существует.'
    EMAIL_EXISTS = 'Пользователь с таким E-mail уже существует.'

    @classmethod
    def compare_passwords(
        cls, password: str, password_confirmation: str
    ) -> None:
        """Сравнение паролей."""
        if not password == password_confirmation:
            raise ValidationError(cls.WRONG_PASSWORD_CONFIRMATION, 'password')

    @classmethod
    def validate_username(cls, username: str) -> None:
        """Проверка на уникальность имени пользователя."""
        username_exists = User.objects.filter(username=username).exists()
        if username_exists:
            raise ValidationError(cls.USERNAME_EXISTS, 'username')

    @classmethod
    def validate_email(cls, email: str) -> None:
        """Проверка на уникальность почнового ящика."""
        email_exists = User.objects.filter(email=email).exists()
        if email_exists:
            raise ValidationError(cls.EMAIL_EXISTS, 'email')

from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

from taskie.api.exceptions import ValidationError


class Authenticator:
    """Класс для работы с аутентификацией пользователя."""

    WRONG_CREDENTIALS = 'Неверный логин или пароль.'

    @staticmethod
    def _generate_access_token(user):
        token, _ = Token.objects.get_or_create(user=user)
        return token.key

    @classmethod
    def login(cls, username, password, request=None):
        """Авторизует пользователя в системе."""
        user = authenticate(request, username=username, password=password)
        if user is not None:
            return user, cls._generate_access_token(user)
        raise ValidationError(cls.WRONG_CREDENTIALS)

    @classmethod
    def logout(cls, token):
        """Логаут пользователя."""
        Token.objects.filter(key=token).delete()

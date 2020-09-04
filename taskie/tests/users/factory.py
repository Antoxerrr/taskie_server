import factory
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    """Фабрика для модели пользователя."""

    class Meta:
        model = User


class TokenFactory(factory.django.DjangoModelFactory):
    """Фабрика для модели токена авторизации."""

    user = factory.SubFactory(UserFactory)

    class Meta:
        model = Token

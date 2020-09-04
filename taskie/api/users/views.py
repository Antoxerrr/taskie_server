from django.forms import model_to_dict
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from taskie.api.serializers import ValidationErrorSerializer
from taskie.api.users.logic.auth import Authenticator
from taskie.api.users.logic.register import Registerer
from taskie.api.users.serializers import (
    RegisterSerializer, LoginSerializer, LoginResponseSerializer)


class BaseAuthViewSet(ViewSet):
    """Вьюсет пользователей."""

    permission_classes = (permissions.AllowAny,)

    @swagger_auto_schema(
        request_body=RegisterSerializer,
        responses={
            status.HTTP_200_OK: 'success',
            status.HTTP_400_BAD_REQUEST: ValidationErrorSerializer
        }
    )
    @action(methods=('post',), detail=False)
    def register(self, request):
        """Эндпоинт на регистрацию пользователя."""
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        Registerer.register(serializer.validated_data)
        return Response(status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=LoginSerializer,
        responses={
            status.HTTP_200_OK: LoginResponseSerializer,
            status.HTTP_400_BAD_REQUEST: ValidationErrorSerializer
        }
    )
    @action(methods=('post',), detail=False)
    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, token = Authenticator.login(
            serializer.validated_data.get('username'),
            serializer.validated_data.get('password'),
            request
        )
        serializer = LoginResponseSerializer(
            data=dict(token=token, user=model_to_dict(user))
        )
        serializer.is_valid(raise_exception=True)
        return Response(
            data=serializer.validated_data, status=status.HTTP_200_OK
        )

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: 'success',
            status.HTTP_401_UNAUTHORIZED: 'unauthorized'
        }
    )
    @action(methods=('post',), detail=False)
    def logout(self, request):
        """Логаут пользователя."""
        if not request.user.is_authenticated or request.auth is None:
            response = Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            Authenticator.logout(request.auth.key)
            response = Response(status=status.HTTP_200_OK)
        return response

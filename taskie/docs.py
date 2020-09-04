from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions


def swagger_urls():
    schema_view = get_schema_view(
        openapi.Info(
            title="Taskie API",
            default_version='v1',
            description="API сервиса Taskie",
        ),
        public=True,
        permission_classes=(permissions.AllowAny,),
    )

    return [
        path(
            'docs/',
            schema_view.with_ui('swagger', cache_timeout=0),
            name='schema-swagger-ui'
        ),
    ]

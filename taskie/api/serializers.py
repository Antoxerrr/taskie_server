from rest_framework import serializers


class ValidationErrorSerializer(serializers.Serializer):
    """Сериализатор ошибки валидации."""

    message = serializers.CharField(required=True, help_text='Текст ошибки')
    is_field_error = serializers.BooleanField(
        required=True, help_text='Относится ли ошибка к полю формы'
    )
    field = serializers.BooleanField(
        required=False, help_text='Название поля, к которому относится ошибка'
    )

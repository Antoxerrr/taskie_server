from rest_framework.exceptions import ValidationError as _ValidationError


class ValidationError(_ValidationError):
    """Ошибка валидации."""

    def __init__(self, detail=None, field=None):
        if detail is None:
            detail = self.default_detail
        self.detail = self._get_error_details(detail, field)

    @staticmethod
    def _get_error_details(detail, field) -> dict:
        is_field_error = bool(field)
        details = dict(
            message=detail,
            is_field_error=is_field_error
        )
        if is_field_error:
            details['field'] = field
        return details

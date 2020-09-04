from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as _UserAdmin

from taskie.api.users.models import User


@admin.register(User)
class UserAdmin(_UserAdmin):
    """Модель админа пользователя."""

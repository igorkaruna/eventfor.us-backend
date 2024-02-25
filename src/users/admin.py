from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from events.models import User


class UserAdmin(BaseUserAdmin):
    list_display: tuple[str, ...] = (
        "email",
        "first_name",
        "last_name",
        "is_active",
        "is_verified",
        "is_superuser",
    )

    list_filter: tuple[str, ...] = ("is_active", "is_verified", "is_superuser")
    search_fields: tuple[str, ...] = ("email", "first_name", "last_name")
    ordering: tuple[str, ...] = ("email",)

    fieldsets: tuple[tuple[str, dict], ...] = (
        (
            None,
            {"fields": ("email", "password")},
        ),
        (
            "Personal Info",
            {"fields": ("first_name", "last_name")},
        ),
        (
            "Permissions",
            {"fields": ("is_active", "is_verified", "is_superuser")},
        ),
    )
    add_fieldsets: tuple[tuple[str, dict], ...] = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "first_name",
                    "last_name",
                    "password1",
                    "password2",
                    "is_active",
                    "is_verified",
                    "is_superuser",
                ),
            },
        ),
    )


admin.site.register(User, UserAdmin)

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):

    list_display = (
        "email",
        "first_name",
        "last_name",
        "role",
        "is_staff",
    )

    ordering = ("email",)

    fieldsets = UserAdmin.fieldsets + (
        (
            "Información adicional",
            {
                "fields": (
                    "phone",
                    "role",
                )
            },
        ),
    )
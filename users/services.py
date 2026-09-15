from django.core.exceptions import ValidationError

from users.models import CustomUser


class UserService:

    @staticmethod
    def create_user(email, password, **extra_fields):

        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError(
                {
                    "email": "Ya existe un usuario con ese email."
                }
            )

        return CustomUser.objects.create_user(
            email=email,
            password=password,
            **extra_fields
        )
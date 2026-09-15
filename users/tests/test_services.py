import pytest
from django.core.exceptions import ValidationError

from users.models import CustomUser
from users.services import UserService


@pytest.mark.django_db
def test_create_user_existing_email():
    CustomUser.objects.create_user(
        email="usuario@example.com",
        username="usuario",
        password="password123",
    )

    with pytest.raises(ValidationError) as exc_info:
        UserService.create_user(
            email="usuario@example.com",
            password="password123",
            username="otro_usuario",
        )

    assert exc_info.value.message_dict == {
        "email": ["Ya existe un usuario con ese email."]
    }
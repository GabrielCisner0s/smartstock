import pytest

from users.models import CustomUser

#este test verifica que el método __str__ del modelo CustomUser devuelva el correo electrónico del usuario correctamente.
@pytest.mark.django_db
def test_custom_user_str():
    user = CustomUser.objects.create_user(
        email="test@example.com",
        username="testuser",
        password="password123",
    )

    assert str(user) == "test@example.com"
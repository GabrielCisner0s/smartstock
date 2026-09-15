import pytest

from users.managers import CustomUserManager
from users.models import CustomUser


@pytest.mark.django_db
def test_create_user():
    manager = CustomUserManager()
    manager.model = CustomUser

    user = manager.create_user(
        email="Usuario@Example.COM",
        password="password123",
        username="usuario",
    )

    assert user.email == "Usuario@example.com"
    assert user.username == "usuario"
    assert user.check_password("password123")
    assert user.is_active is True


def test_create_user_without_email():
    manager = CustomUserManager()
    manager.model = CustomUser

    with pytest.raises(ValueError, match="El email es obligatorio."):
        manager.create_user(
            email="",
            password="password123",
            username="usuario",
        )


@pytest.mark.django_db
def test_create_superuser():
    manager = CustomUserManager()
    manager.model = CustomUser

    user = manager.create_superuser(
        email="admin@example.com",
        password="password123",
        username="admin",
    )

    assert user.email == "admin@example.com"
    assert user.is_staff is True
    assert user.is_superuser is True
    assert user.is_active is True


def test_create_superuser_without_staff():
    manager = CustomUserManager()
    manager.model = CustomUser

    with pytest.raises(
        ValueError,
        match="El superusuario debe tener is_staff=True.",
    ):
        manager.create_superuser(
            email="admin@example.com",
            password="password123",
            username="admin",
            is_staff=False,
        )


def test_create_superuser_without_superuser():
    manager = CustomUserManager()
    manager.model = CustomUser

    with pytest.raises(
        ValueError,
        match="El superusuario debe tener is_superuser=True.",
    ):
        manager.create_superuser(
            email="admin@example.com",
            password="password123",
            username="admin",
            is_superuser=False,
        )
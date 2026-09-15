from django.contrib.auth.models import AbstractUser
from django.db import models

from .managers import CustomUserManager


class CustomUser(AbstractUser):

    #username = models.CharField(max_length=150, unique=True)

    email = models.EmailField(unique=True)

    phone = models.CharField(
        max_length=20,
        blank=True
    )

    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Administrador"
        SUPERVISOR = "SUPERVISOR", "Supervisor"
        EMPLOYEE = "EMPLOYEE", "Empleado"

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.EMPLOYEE
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = [
        "username",
        "first_name",
        "last_name",
    ]

    def __str__(self):
        return self.email
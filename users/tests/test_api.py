import pytest

from rest_framework import status
from rest_framework.test import APIClient

from users.tests.factories import UserFactory

#REGISTRO DE USUARIO CORRECTO
@pytest.mark.django_db
def test_register_user():

    client = APIClient()

    data = {
        "email": "nuevo@example.com",
        "username": "nuevo_usuario",
        "first_name": "Nuevo",
        "last_name": "Usuario",
        "phone": "3815555555",
        "password": "Password123!",
    }

    response = client.post(
        "/api/auth/register/",
        data,
        format="json",
    )

    print(response.data)

    assert response.status_code == status.HTTP_201_CREATED

    assert response.data["email"] == "nuevo@example.com"
    

#REGISTRO CON EMAIL DUPLICADO
@pytest.mark.django_db
def test_register_user_duplicate_email():

    UserFactory(
        email="usuario@example.com"
    )

    client = APIClient()

    data = {
        "email": "usuario@example.com",
        "username": "otro_usuario",
        "first_name": "Otro",
        "last_name": "Usuario",
        "phone": "3815555555",
        "password": "Password123!",
    }

    response = client.post(
        "/api/auth/register/",
        data,
        format="json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    


#LOGIN CORRECTO
@pytest.mark.django_db
def test_login_success():

    user = UserFactory(
        email="login@example.com"
    )

    user.set_password("Password123!")
    user.save()

    client = APIClient()

    response = client.post(
        "/api/auth/login/",
        {
            "email": "login@example.com",
            "password": "Password123!",
        },
        format="json",
    )

    assert response.status_code == status.HTTP_200_OK

    assert "access" in response.data
    assert "refresh" in response.data
    
   
   
   
#LOGIN INCORRECTO 
@pytest.mark.django_db
def test_login_invalid_password():

    user = UserFactory(
        email="login@example.com"
    )

    user.set_password("Password123!")
    user.save()

    client = APIClient()

    response = client.post(
        "/api/auth/login/",
        {
            "email": "login@example.com",
            "password": "password_incorrecta",
        },
        format="json",
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    
#REFRESH TOKEN CORRECTO
@pytest.mark.django_db
def test_refresh_token():

    user = UserFactory(
        email="refresh@example.com"
    )

    user.set_password("Password123!")
    user.save()

    client = APIClient()

    login_response = client.post(
        "/api/auth/login/",
        {
            "email": "refresh@example.com",
            "password": "Password123!",
        },
        format="json",
    )

    refresh_token = login_response.data["refresh"]

    response = client.post(
        "/api/auth/refresh/",
        {
            "refresh": refresh_token,
        },
        format="json",
    )

    assert response.status_code == status.HTTP_200_OK

    assert "access" in response.data
    
    
#PROFILE AUTENTICADO
@pytest.mark.django_db
def test_profile_authenticated():

    user = UserFactory(
        email="profile@example.com"
    )

    client = APIClient()

    client.force_authenticate(
        user=user
    )

    response = client.get(
        "/api/auth/profile/"
    )

    assert response.status_code == status.HTTP_200_OK

    assert response.data["email"] == user.email
    

#PROFILE NO AUTENTICADO
@pytest.mark.django_db
def test_profile_unauthenticated():

    client = APIClient()

    response = client.get(
        "/api/auth/profile/"
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
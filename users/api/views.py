from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated

from .serializers import (
    ProfileSerializer,
    RegisterSerializer,
)

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from drf_spectacular.utils import (
    extend_schema,
    OpenApiResponse,
)



@extend_schema(
    tags=["Authentication"],
    summary="Login",
    description=(
        "Autentica un usuario mediante email y contraseña "
        "y devuelve un access token y un refresh token."
    ),
)
class LoginView(TokenObtainPairView):
    pass


@extend_schema(
    tags=["Authentication"],
    summary="Refresh access token",
    description=(
        "Genera un nuevo access token utilizando "
        "un refresh token válido."
    ),
)
class RefreshTokenView(TokenRefreshView):
    pass

@extend_schema(
    tags=["Users"],
    summary="Register user",
    description=(
        "Crea un nuevo usuario en el sistema. "
        "No requiere autenticación."
    ),
    request=RegisterSerializer,
    responses={
        201: OpenApiResponse(
            response=RegisterSerializer,
            description="Usuario creado correctamente.",
        ),
        400: OpenApiResponse(
            description="Los datos enviados no son válidos.",
        ),
    },
)
class RegisterView(generics.CreateAPIView):

    serializer_class = RegisterSerializer

    permission_classes = [
        AllowAny
    ]


@extend_schema(
    tags=["Users"],
    summary="Get authenticated user profile",
    description=(
        "Obtiene los datos del usuario actualmente autenticado."
    ),
    responses={
        200: OpenApiResponse(
            response=ProfileSerializer,
            description="Perfil obtenido correctamente.",
        ),
        401: OpenApiResponse(
            description="No autenticado.",
        ),
    },
)
class ProfileView(generics.RetrieveAPIView):

    serializer_class = ProfileSerializer

    permission_classes = [
        IsAuthenticated
    ]

    def get_object(self):
        return self.request.user
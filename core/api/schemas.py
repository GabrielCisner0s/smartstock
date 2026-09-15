from drf_spectacular.utils import OpenApiResponse


UNAUTHORIZED_RESPONSE = OpenApiResponse(
    description="No se proporcionaron credenciales válidas."
)

FORBIDDEN_RESPONSE = OpenApiResponse(
    description="El usuario autenticado no tiene permisos suficientes."
)
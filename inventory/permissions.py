from rest_framework.permissions import BasePermission


from users.models import CustomUser
class InventoryPermission(BasePermission):
    """
    Permisos para las operaciones de inventario.

    ADMIN:
        - Puede consultar
        - Puede registrar movimientos
        - Puede modificar/eliminar si el endpoint lo permite

    SUPERVISOR:
        - Puede consultar
        - Puede registrar movimientos

    EMPLOYEE:
        - Puede consultar
        - Puede registrar movimientos
    """

    def has_permission(self, request, view):

        user = request.user

        # Usuario no autenticado
        if not user.is_authenticated:
            return False

        role = user.role

        # Lectura
        if request.method in (
            "GET",
            "HEAD",
            "OPTIONS",
        ):
            return role in (
                "ADMIN",
                "SUPERVISOR",
                "EMPLOYEE",
            )

        # Crear movimiento
        if request.method == "POST":
            return role in (
                "ADMIN",
                "SUPERVISOR",
                "EMPLOYEE",
            )

        # Modificar
        if request.method in (
            "PUT",
            "PATCH",
        ):
            return role in (
                "ADMIN",
                "SUPERVISOR",
            )

        # Eliminar
        if request.method == "DELETE":
            return role == "ADMIN"

        return False
    
class InventoryReportPermission(BasePermission):
    """
    Los reportes de inventario están disponibles
    solamente para ADMIN y SUPERVISOR.
    """

    def has_permission(self, request, view):

        if not request.user.is_authenticated:
            return False

        return request.user.role in (
            CustomUser.Role.ADMIN,
            CustomUser.Role.SUPERVISOR,
        )
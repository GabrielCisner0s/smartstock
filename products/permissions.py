from rest_framework.permissions import BasePermission, SAFE_METHODS

from users.models import CustomUser


class ProductPermission(BasePermission):
    """
    Permisos para el módulo de productos.

    ADMIN:
        Puede realizar cualquier operación.

    SUPERVISOR:
        Puede consultar, crear y modificar productos.

    EMPLOYEE:
        Puede solamente consultar productos.
    """

   

    def has_permission(self, request, view):

        if not request.user.is_authenticated:
            return False

        if request.method in SAFE_METHODS:
            return True

        if request.user.role == CustomUser.Role.ADMIN:
            return True

        if (
            request.user.role == CustomUser.Role.SUPERVISOR
            and request.method in ("POST", "PUT", "PATCH")
        ):
            return True

        return False


class IsAdmin(BasePermission):

    def has_permission(self, request, view):

        return (
            request.user.is_authenticated
            and request.user.role == CustomUser.Role.ADMIN
        )


class IsSupervisor(BasePermission):

    def has_permission(self, request, view):

        return (
            request.user.is_authenticated
            and request.user.role == CustomUser.Role.SUPERVISOR
        )


class IsEmployee(BasePermission):

    def has_permission(self, request, view):

        return (
            request.user.is_authenticated
            and request.user.role == CustomUser.Role.EMPLOYEE
        )
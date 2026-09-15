import pytest
from rest_framework.test import APIRequestFactory
from users.tests.factories import UserFactory
from django.contrib.auth.models import AnonymousUser
from products.permissions import (
    ProductPermission,
    IsAdmin,
    IsSupervisor,
    IsEmployee,
)
from users.models import CustomUser
from products.tests.factories import UserFactory

@pytest.mark.django_db
def test_admin_has_full_access():

    request = APIRequestFactory().post(
        "/api/products/"
    )

    request.user = UserFactory(
        role="ADMIN"
    )

    permission = ProductPermission()

    assert permission.has_permission(
        request,
        None,
    )


@pytest.mark.django_db
def test_supervisor_can_create():

    request = APIRequestFactory().post(
        "/api/products/"
    )

    request.user = UserFactory(
        role="SUPERVISOR"
    )

    permission = ProductPermission()

    assert permission.has_permission(
        request,
        None,
    )


@pytest.mark.django_db
def test_employee_cannot_create():

    request = APIRequestFactory().post(
        "/api/products/"
    )

    request.user = UserFactory(
        role="EMPLOYEE"
    )

    permission = ProductPermission()

    assert not permission.has_permission(
        request,
        None,
    )


@pytest.mark.django_db
def test_employee_can_read():

    request = APIRequestFactory().get(
        "/api/products/"
    )

    request.user = UserFactory(
        role="EMPLOYEE"
    )

    permission = ProductPermission()

    assert permission.has_permission(
        request,
        None,
    )


@pytest.mark.django_db
def test_supervisor_can_update():

    request = APIRequestFactory().patch(
        "/api/products/1/",
        {},
        format="json",
    )

    request.user = UserFactory(
        role="SUPERVISOR"
    )

    permission = ProductPermission()

    assert permission.has_permission(
        request,
        None,
    )


@pytest.mark.django_db
def test_employee_cannot_update():

    request = APIRequestFactory().patch(
        "/api/products/1/",
        {},
        format="json",
    )

    request.user = UserFactory(
        role="EMPLOYEE"
    )

    permission = ProductPermission()

    assert not permission.has_permission(
        request,
        None,
    )


@pytest.mark.django_db
def test_only_admin_can_delete():

    request = APIRequestFactory().delete(
        "/api/products/1/"
    )

    request.user = UserFactory(
        role="SUPERVISOR"
    )

    permission = ProductPermission()

    assert not permission.has_permission(
        request,
        None,
    )


@pytest.mark.django_db
def test_admin_can_delete():

    request = APIRequestFactory().delete(
        "/api/products/1/"
    )

    request.user = UserFactory(
        role="ADMIN"
    )

    permission = ProductPermission()

    assert permission.has_permission(
        request,
        None,
    )



@pytest.mark.django_db
class TestProductPermission:

    def setup_method(self):
        self.factory = APIRequestFactory()
        self.permission = ProductPermission()

    def test_anonymous_user_is_denied(self):
        request = self.factory.get("/products/")
        request.user = AnonymousUser()

        assert self.permission.has_permission(request, None) is False

    def test_authenticated_user_can_read(self):
        user = UserFactory(role=CustomUser.Role.EMPLOYEE)

        request = self.factory.get("/products/")
        request.user = user

        assert self.permission.has_permission(request, None) is True

    def test_admin_can_perform_any_operation(self):
        user = UserFactory(role=CustomUser.Role.ADMIN)

        for method in ("POST", "PUT", "PATCH", "DELETE"):
            request = getattr(self.factory, method.lower())("/products/")
            request.user = user

            assert self.permission.has_permission(request, None) is True

    def test_supervisor_can_create_and_modify(self):
        user = UserFactory(role=CustomUser.Role.SUPERVISOR)

        for method in ("POST", "PUT", "PATCH"):
            request = getattr(self.factory, method.lower())("/products/")
            request.user = user

            assert self.permission.has_permission(request, None) is True

    def test_supervisor_cannot_delete(self):
        user = UserFactory(role=CustomUser.Role.SUPERVISOR)

        request = self.factory.delete("/products/")
        request.user = user

        assert self.permission.has_permission(request, None) is False

    def test_employee_cannot_modify(self):
        user = UserFactory(role=CustomUser.Role.EMPLOYEE)

        request = self.factory.post("/products/")
        request.user = user

        assert self.permission.has_permission(request, None) is False

    def test_unsupported_method_is_denied(self):
        user = UserFactory(role=CustomUser.Role.EMPLOYEE)

        request = self.factory.delete("/products/")
        request.user = user

        assert self.permission.has_permission(request, None) is False


class TestRolePermissions:

    @pytest.mark.django_db
    def test_is_admin_allows_admin(self):
        user = UserFactory(role=CustomUser.Role.ADMIN)

        request = APIRequestFactory().get("/")
        request.user = user

        assert IsAdmin().has_permission(request, None) is True

    @pytest.mark.django_db
    def test_is_admin_denies_non_admin(self):
        user = UserFactory(role=CustomUser.Role.EMPLOYEE)

        request = APIRequestFactory().get("/")
        request.user = user

        assert IsAdmin().has_permission(request, None) is False

    @pytest.mark.django_db
    def test_is_supervisor_allows_supervisor(self):
        user = UserFactory(role=CustomUser.Role.SUPERVISOR)

        request = APIRequestFactory().get("/")
        request.user = user

        assert IsSupervisor().has_permission(request, None) is True

    @pytest.mark.django_db
    def test_is_supervisor_denies_non_supervisor(self):
        user = UserFactory(role=CustomUser.Role.EMPLOYEE)

        request = APIRequestFactory().get("/")
        request.user = user

        assert IsSupervisor().has_permission(request, None) is False

    @pytest.mark.django_db
    def test_is_employee_allows_employee(self):
        user = UserFactory(role=CustomUser.Role.EMPLOYEE)

        request = APIRequestFactory().get("/")
        request.user = user

        assert IsEmployee().has_permission(request, None) is True

    @pytest.mark.django_db
    def test_is_employee_denies_non_employee(self):
        user = UserFactory(role=CustomUser.Role.ADMIN)

        request = APIRequestFactory().get("/")
        request.user = user

        assert IsEmployee().has_permission(request, None) is False
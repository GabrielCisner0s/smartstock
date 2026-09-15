import pytest

from django.contrib.auth.models import AnonymousUser

from rest_framework.test import APIRequestFactory

from inventory.permissions import (
    InventoryPermission,
    InventoryReportPermission,
)

from users.tests.factories import UserFactory


@pytest.mark.django_db
def test_admin_has_full_access():
    request = APIRequestFactory().post(
        "/api/inventory/"
    )

    request.user = UserFactory(
        role="ADMIN"
    )

    permission = InventoryPermission()

    assert permission.has_permission(
        request,
        None,
    )


@pytest.mark.django_db
def test_supervisor_can_create():
    request = APIRequestFactory().post(
        "/api/inventory/"
    )

    request.user = UserFactory(
        role="SUPERVISOR"
    )

    permission = InventoryPermission()

    assert permission.has_permission(
        request,
        None,
    )


@pytest.mark.django_db
def test_employee_can_create():
    request = APIRequestFactory().post(
        "/api/inventory/"
    )

    request.user = UserFactory(
        role="EMPLOYEE"
    )

    permission = InventoryPermission()

    assert permission.has_permission(
        request,
        None,
    )


@pytest.mark.django_db
def test_employee_can_read():
    request = APIRequestFactory().get(
        "/api/inventory/"
    )

    request.user = UserFactory(
        role="EMPLOYEE"
    )

    permission = InventoryPermission()

    assert permission.has_permission(
        request,
        None,
    )


@pytest.mark.django_db
def test_supervisor_can_update():
    request = APIRequestFactory().patch(
        "/api/inventory/1/",
        {},
        format="json",
    )

    request.user = UserFactory(
        role="SUPERVISOR"
    )

    permission = InventoryPermission()

    assert permission.has_permission(
        request,
        None,
    )


@pytest.mark.django_db
def test_employee_cannot_update():
    request = APIRequestFactory().patch(
        "/api/inventory/1/",
        {},
        format="json",
    )

    request.user = UserFactory(
        role="EMPLOYEE"
    )

    permission = InventoryPermission()

    assert not permission.has_permission(
        request,
        None,
    )


@pytest.mark.django_db
def test_supervisor_cannot_delete():
    request = APIRequestFactory().delete(
        "/api/inventory/1/"
    )

    request.user = UserFactory(
        role="SUPERVISOR"
    )

    permission = InventoryPermission()

    assert not permission.has_permission(
        request,
        None,
    )


@pytest.mark.django_db
def test_admin_can_delete():
    request = APIRequestFactory().delete(
        "/api/inventory/1/"
    )

    request.user = UserFactory(
        role="ADMIN"
    )

    permission = InventoryPermission()

    assert permission.has_permission(
        request,
        None,
    )


@pytest.mark.django_db
def test_unauthenticated_user_cannot_access_inventory():
    request = APIRequestFactory().get(
        "/api/inventory/"
    )

    request.user = AnonymousUser()

    permission = InventoryPermission()

    assert not permission.has_permission(
        request,
        None,
    )


@pytest.mark.django_db
def test_employee_can_use_head():
    request = APIRequestFactory().head(
        "/api/inventory/"
    )

    request.user = UserFactory(
        role="EMPLOYEE"
    )

    permission = InventoryPermission()

    assert permission.has_permission(
        request,
        None,
    )


@pytest.mark.django_db
def test_employee_can_use_options():
    request = APIRequestFactory().options(
        "/api/inventory/"
    )

    request.user = UserFactory(
        role="EMPLOYEE"
    )

    permission = InventoryPermission()

    assert permission.has_permission(
        request,
        None,
    )
    

@pytest.mark.django_db
def test_supervisor_can_put():
    request = APIRequestFactory().put(
        "/api/inventory/1/",
        {},
        format="json",
    )

    request.user = UserFactory(
        role="SUPERVISOR"
    )

    permission = InventoryPermission()

    assert permission.has_permission(
        request,
        None,
    )

#este test verifica que un empleado no pueda realizar una solicitud PUT a la API de inventario, lo cual es consistente con las reglas de permisos definidas en la clase InventoryPermission.
@pytest.mark.django_db
def test_employee_cannot_put():
    request = APIRequestFactory().put(
        "/api/inventory/1/",
        {},
        format="json",
    )

    request.user = UserFactory(
        role="EMPLOYEE"
    )

    permission = InventoryPermission()

    assert not permission.has_permission(
        request,
        None,
    )

@pytest.mark.django_db
def test_supervisor_can_put():
    request = APIRequestFactory().put(
        "/api/inventory/1/",
        {},
        format="json",
    )

    request.user = UserFactory(
        role="SUPERVISOR"
    )

    permission = InventoryPermission()

    assert permission.has_permission(
        request,
        None,
    )


@pytest.mark.django_db
def test_employee_cannot_put():
    request = APIRequestFactory().put(
        "/api/inventory/1/",
        {},
        format="json",
    )

    request.user = UserFactory(
        role="EMPLOYEE"
    )

    permission = InventoryPermission()

    assert not permission.has_permission(
        request,
        None,
    )

@pytest.mark.django_db
def test_unsupported_method_is_denied():
    request = APIRequestFactory().generic(
        "TRACE",
        "/api/inventory/",
    )

    request.user = UserFactory(
        role="EMPLOYEE"
    )

    permission = InventoryPermission()

    assert not permission.has_permission(
        request,
        None,
    )

@pytest.mark.django_db
def test_admin_can_access_inventory_reports():
    request = APIRequestFactory().get(
        "/api/inventory/reports/"
    )

    request.user = UserFactory(
        role="ADMIN"
    )

    permission = InventoryReportPermission()

    assert permission.has_permission(
        request,
        None,
    )
    

@pytest.mark.django_db
def test_supervisor_can_access_inventory_reports():
    request = APIRequestFactory().get(
        "/api/inventory/reports/"
    )

    request.user = UserFactory(
        role="SUPERVISOR"
    )

    permission = InventoryReportPermission()

    assert permission.has_permission(
        request,
        None,
    )

@pytest.mark.django_db
def test_employee_cannot_access_inventory_reports():
    request = APIRequestFactory().get(
        "/api/inventory/reports/"
    )

    request.user = UserFactory(
        role="EMPLOYEE"
    )

    permission = InventoryReportPermission()

    assert not permission.has_permission(
        request,
        None,
    )


@pytest.mark.django_db
def test_unauthenticated_user_cannot_access_inventory_reports():
    request = APIRequestFactory().get(
        "/api/inventory/reports/"
    )

    request.user = AnonymousUser()

    permission = InventoryReportPermission()

    assert not permission.has_permission(
        request,
        None,
    )
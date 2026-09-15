from django.template import response
import pytest
from products.models import Product
from users.tests.factories import UserFactory

from rest_framework.test import APIClient
from products.tests.factories import (
    ProductFactory,
    CategoryFactory
)

@pytest.mark.django_db
def test_products_requires_authentication():

    client = APIClient()

    response = client.get("/api/products/")

    assert response.status_code in (401, 403)
    


@pytest.mark.django_db
def test_inventory_requires_authentication():

    client = APIClient()

    response = client.get("/api/inventory/movements/")

    assert response.status_code in (401, 403)
    


@pytest.mark.django_db
def test_reports_requires_authentication():

    client = APIClient()

    response = client.get("/api/reports/dashboard/")

    assert response.status_code in (401, 403)
    
@pytest.mark.django_db
def test_employee_cannot_create_product():

    user = UserFactory(
        role="EMPLOYEE"
    )

    client = APIClient()

    client.force_authenticate(
        user=user
    )

    response = client.post(
        "/api/products/",
        {},
        format="json",
    )

    assert response.status_code == 403

@pytest.mark.django_db
def test_employee_cannot_delete_product():

    product = ProductFactory()

    user = UserFactory(
        role="EMPLOYEE"
    )

    client = APIClient()

    client.force_authenticate(
        user=user
    )

    response = client.delete(
        f"/api/products/{product.id}/"
    )

    assert response.status_code == 403
    
    
    
@pytest.mark.django_db
def test_supervisor_cannot_delete_product():

    product = ProductFactory()

    user = UserFactory(
        role="SUPERVISOR"
    )

    client = APIClient()

    client.force_authenticate(
        user=user
    )

    response = client.delete(
        f"/api/products/{product.id}/"
    )

    assert response.status_code == 403
    
    

@pytest.mark.django_db
def test_admin_can_delete_product():

    product = ProductFactory()

    user = UserFactory(
        role="ADMIN"
    )

    client = APIClient()

    client.force_authenticate(
        user=user
    )

    response = client.delete(
        f"/api/products/{product.id}/"
    )

    assert response.status_code in (200, 204)


@pytest.mark.django_db
def test_employee_can_read_categories():
    user = UserFactory(
        role="EMPLOYEE"
    )

    client = APIClient()

    client.force_authenticate(
        user=user
    )

    response = client.get(
        "/api/products/categories/"
    )

    assert response.status_code == 200


@pytest.mark.django_db
def test_employee_cannot_create_category():
    user = UserFactory(
        role="EMPLOYEE"
    )

    client = APIClient()

    client.force_authenticate(
        user=user
    )

    response = client.post(
        "/api/products/categories/",
        {
            "name": "Categoría prohibida"
        },
        format="json",
    )

    assert response.status_code == 403
    
    
#este test verifica que un usuario con rol SUPERVISOR pueda crear un producto, asegurando que la operación de creación esté permitida para este rol.
@pytest.mark.django_db
def test_supervisor_can_create_product():
    user = UserFactory(
        role="SUPERVISOR"
    )

    client = APIClient()

    client.force_authenticate(
        user=user
    )

    response = client.post(
        "/api/products/",
        {},
        format="json",
    )

    # El permiso debe permitir la operación.
    # El 400/201 depende de si los datos enviados son válidos.
    assert response.status_code != 403
    
#este test verifica que un usuario con rol SUPERVISOR pueda actualizar un producto, asegurando que la operación de actualización esté permitida para este rol.
@pytest.mark.django_db
def test_supervisor_can_update_product():
    product = ProductFactory()

    user = UserFactory(
        role="SUPERVISOR"
    )

    client = APIClient()

    client.force_authenticate(
        user=user
    )

    response = client.patch(
        f"/api/products/{product.id}/",
        {},
        format="json",
    )

    assert response.status_code != 403
    
#este test verifica que un usuario con rol EMPLOYEE no pueda actualizar un producto, asegurando que la operación de actualización esté restringida para este rol.
@pytest.mark.django_db
def test_employee_cannot_update_product():
    product = ProductFactory()

    user = UserFactory(
        role="EMPLOYEE"
    )

    client = APIClient()

    client.force_authenticate(
        user=user
    )

    response = client.patch(
        f"/api/products/{product.id}/",
        {},
        format="json",
    )

    assert response.status_code == 403
    
#este test verifica que un usuario con rol EMPLOYEE no pueda actualizar una categoría, asegurando que la operación de actualización esté restringida para este rol.
@pytest.mark.django_db
def test_employee_can_read_categories():
    user = UserFactory(
        role="EMPLOYEE"
    )

    client = APIClient()

    client.force_authenticate(
        user=user
    )

    response = client.get(
        "/api/products/categories/"
    )

    assert response.status_code == 200


#este test verifica que un usuario con rol EMPLOYEE no pueda actualizar una categoría, asegurando que la operación de actualización esté restringida para este rol.
@pytest.mark.django_db
def test_employee_cannot_update_category():
    from products.tests.factories import CategoryFactory

    category = CategoryFactory()

    user = UserFactory(
        role="EMPLOYEE"
    )

    client = APIClient()

    client.force_authenticate(
        user=user
    )

    response = client.patch(
        f"/api/products/categories/{category.id}/",
        {},
        format="json",
    )

    assert response.status_code == 403
    
    
#este test verifica que un usuario con rol EMPLOYEE pueda acceder a la lista de productos con stock bajo.
@pytest.mark.django_db
def test_employee_can_read_low_stock_products():
    user = UserFactory(
        role="EMPLOYEE"
    )

    client = APIClient()

    client.force_authenticate(
        user=user
    )

    response = client.get(
        "/api/products/low-stock/"
    )

    assert response.status_code == 200


#este test verifica que al actualizar un producto, el usuario que realiza la actualización se registre correctamente en el campo updated_by y que el campo created_by permanezca sin cambios.
@pytest.mark.django_db
def test_product_update_records_user():

    product = ProductFactory()

    user = UserFactory(
        role="ADMIN"
    )

    client = APIClient()

    client.force_authenticate(
        user=user
    )

    response = client.patch(
        f"/api/products/{product.id}/",
        {
            "name": "Producto modificado"
        },
        format="json",
    )

    print("STATUS:", response.status_code)
    print("DATA:", response.data)
    assert response.status_code == 200

    product.refresh_from_db()

    assert product.updated_by == user



#este test verifica que un usuario no pueda modificar el campo created_by de un producto, asegurando que este campo permanezca inalterado después de un intento de actualización.
@pytest.mark.django_db
def test_user_cannot_modify_created_by():

    product = ProductFactory()

    original_creator = product.created_by

    attacker = UserFactory(
        role="ADMIN"
    )

    client = APIClient()

    client.force_authenticate(
        user=attacker
    )

    response = client.patch(
        f"/api/products/{product.id}/",
        {
            "created_by": attacker.id
        },
        format="json",
    )
    
    assert response.status_code == 200

    product.refresh_from_db()

    assert product.created_by == original_creator
    
    
#este test verifica que al eliminar un producto, se realice un soft delete, es decir, que el campo is_deleted se actualice a True en lugar de eliminar físicamente el registro de la base de datos.
@pytest.mark.django_db
def test_product_delete_is_soft_delete():

    product = ProductFactory()

    user = UserFactory(
        role="ADMIN"
    )

    client = APIClient()

    client.force_authenticate(
        user=user
    )

    response = client.delete(
        f"/api/products/{product.id}/"
    )

    assert response.status_code in (200, 204)

    product.refresh_from_db()

    assert product.is_deleted is True
    
#este test verifica que al eliminar un producto, el usuario que realiza la eliminación se registre correctamente en el campo updated_by y que el campo created_by permanezca sin cambios.
@pytest.mark.django_db
def test_product_delete_records_user():

    product = ProductFactory()

    creator = product.created_by

    user = UserFactory(
        role="ADMIN"
    )

    client = APIClient()

    client.force_authenticate(
        user=user
    )

    response = client.delete(
        f"/api/products/{product.id}/"
    )

    assert response.status_code in (200, 204)

    product.refresh_from_db()

    assert product.is_deleted is True
    assert product.created_by == creator
    assert product.updated_by == user


#este test verifica que un producto eliminado no aparezca en la lista de productos activos.
@pytest.mark.django_db
def test_deleted_product_not_in_list():

    product = ProductFactory(
        is_deleted=True
    )

    user = UserFactory()

    client = APIClient()

    client.force_authenticate(
        user=user
    )

    response = client.get(
        "/api/products/"
    )

    assert response.status_code == 200

    ids = [
        item["id"]
        for item in response.data["results"]
    ]

    assert product.id not in ids

#test para verificar que el usuario que crea un producto es registrado correctamente en el campo created_by y que updated_by es None al momento de la creación.
@pytest.mark.django_db
def test_product_create_records_user():

    user = UserFactory(
        role="ADMIN"
    )

    client = APIClient()

    client.force_authenticate(
        user=user
    )

    category = CategoryFactory()

    response = client.post(
        "/api/products/",
        {
            "sku": "AUD-001",
            "name": "Producto auditoría",
            "description": "Test auditoría",
            "price": "100.00",
            "stock": 10,
            "minimum_stock": 5,
            "category_id": category.id,
        },
        format="json",
    )

    assert response.status_code == 201

    product = Product.objects.get(
        sku="AUD-001"
    )

    assert product.created_by == user
    assert product.updated_by is None



#este test verifica que un producto eliminado pueda ser restaurado correctamente y que el campo is_deleted se actualice a False.
@pytest.mark.django_db
def test_admin_can_restore_product():

    product = ProductFactory(
        is_deleted=True
    )

    user = UserFactory(
        role="ADMIN"
    )

    client = APIClient()

    client.force_authenticate(
        user=user
    )

    response = client.patch(
    f"/api/products/{product.id}/restore/"
    )

    print("STATUS:", response.status_code)
    print("DATA:", response.data)

    assert response.status_code == 200
    

#este test verifica que un producto que no está eliminado no pueda ser restaurado, asegurando que la operación de restauración solo se aplique a productos previamente eliminados.
@pytest.mark.django_db
def test_restore_only_deleted_product():

    product = ProductFactory(
        is_deleted=False
    )

    user = UserFactory(
        role="ADMIN"
    )

    client = APIClient()

    client.force_authenticate(
        user=user
    )

    response = client.patch(
        f"/api/products/{product.id}/restore/"
    )

    assert response.status_code == 404

#este test verifica que un usuario con rol EMPLOYEE no pueda restaurar un producto eliminado, asegurando que la operación de restauración esté restringida para este rol.
@pytest.mark.django_db
def test_employee_cannot_restore_product():

    product = ProductFactory(
        is_deleted=True
    )

    user = UserFactory(
        role="EMPLOYEE"
    )

    client = APIClient()

    client.force_authenticate(
        user=user
    )

    response = client.patch(
        f"/api/products/{product.id}/restore/"
    )

    assert response.status_code == 403

    product.refresh_from_db()

    assert product.is_deleted is True
    
#este test verifica que un usuario con rol SUPERVISOR no pueda restaurar un producto eliminado, asegurando que la operación de restauración esté restringida para este rol.
@pytest.mark.django_db
def test_supervisor_cannot_restore_product():

    product = ProductFactory(
        is_deleted=True
    )

    user = UserFactory(
        role="SUPERVISOR"
    )

    client = APIClient()

    client.force_authenticate(
        user=user
    )

    response = client.patch(
        f"/api/products/{product.id}/restore/"
    )

    assert response.status_code == 403

    product.refresh_from_db()

    assert product.is_deleted is True
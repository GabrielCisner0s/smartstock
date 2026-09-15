from jsonschema import ValidationError
import pytest
from rest_framework.test import APIClient
from inventory.api.serializers import StockMovementSerializer
from inventory.tests.factories import StockMovementFactory
from rest_framework_simplejwt.tokens import RefreshToken
from inventory.models import StockMovement
from products.tests.factories import ProductFactory
from users.tests.factories import UserFactory
from django.utils import timezone
from inventory.api.views import InventoryReportView
from rest_framework.exceptions import ValidationError




#test para crear un movimiento de entrada de inventario a través del endpoint de la API
@pytest.mark.django_db
def test_create_entry_movement_authenticated():

    user = UserFactory()

    product = ProductFactory(
        stock=10
    )

    refresh = RefreshToken.for_user(user)


    client = APIClient()

    client.credentials(
        HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}"
    )


    response = client.post(
        "/api/inventory/movements/",
        {
            "product_id": product.id,
            "movement_type": "ENTRY",
            "quantity": 5,
            "reason": "Compra proveedor",
        },
        format="json",
    )


    assert response.status_code == 201


    product.refresh_from_db()


    assert product.stock == 15


    movement = StockMovement.objects.get(
        id=response.data["id"]
    )


    assert movement.created_by == user

    assert movement.quantity == 5

    assert movement.movement_type == "ENTRY"



#test para crear un movimiento de salida de inventario a través del endpoint de la API
@pytest.mark.django_db
def test_create_movement_without_authentication():

    product = ProductFactory()


    client = APIClient()


    response = client.post(
        "/api/inventory/movements/",
        {
            "product_id": product.id,
            "movement_type": "ENTRY",
            "quantity": 5,
            "reason": "Compra",
        },
        format="json",
    )


    assert response.status_code == 401



#test para obtener los movimientos de inventario a través del endpoint de la API
@pytest.mark.django_db
def test_get_movements():

    user = UserFactory()

    StockMovementFactory.create_batch(3)


    client = APIClient()

    client.force_authenticate(
        user=user
    )


    response = client.get(
        "/api/inventory/movements/"
    )


    assert response.status_code == 200

    assert response.data["count"] == 3
    assert len(response.data["results"]) == 3
    

#test para el endpoint de reportes de inventario
@pytest.mark.django_db
def test_inventory_report():

    user = UserFactory()

    StockMovementFactory.create_batch(3)

    today = timezone.now().date()

    client = APIClient()

    client.force_authenticate(
        user=user
    )

    response = client.get(
        "/api/inventory/reports/",
        {
            "start": today,
            "end": today,
        },
    )

    assert response.status_code == 200
    assert response.data["count"] == 3
    assert len(response.data["results"]) == 3
    
    


#test para el endpoint de reportes de inventario sin fechas
@pytest.mark.django_db
def test_inventory_report_without_dates():

    user = UserFactory()

    client = APIClient()

    client.force_authenticate(
        user=user
    )

    response = client.get(
        "/api/inventory/reports/"
    )

    assert response.status_code == 400
    
#este test verifica que se pueda obtener el detalle de un movimiento de inventario a través del endpoint de la API
@pytest.mark.django_db
def test_get_movement_detail():
    user = UserFactory()

    movement = StockMovementFactory()

    client = APIClient()
    client.force_authenticate(
        user=user
    )

    response = client.get(
        f"/api/inventory/movements/{movement.id}/"
    )

    assert response.status_code == 200
    assert response.data["id"] == movement.id
    
    
#este test verifica que se obtenga un error 404 al intentar obtener el detalle de un movimiento de inventario que no existe a través del endpoint de la API
@pytest.mark.django_db
def test_get_movement_detail_not_found():
    user = UserFactory()

    client = APIClient()
    client.force_authenticate(
        user=user
    )

    response = client.get(
        "/api/inventory/movements/999999/"
    )

    assert response.status_code == 404
    
    
#este test verifica que se pueda obtener un resumen de inventario a través del endpoint de la API
@pytest.mark.django_db
def test_inventory_summary():
    user = UserFactory()
    product = ProductFactory()

    StockMovementFactory(
        product=product,
        movement_type=StockMovement.MovementType.ENTRY,
        quantity=10,
    )

    StockMovementFactory(
        product=product,
        movement_type=StockMovement.MovementType.EXIT,
        quantity=4,
    )

    client = APIClient()
    client.force_authenticate(
        user=user
    )

    response = client.get(
    "/api/inventory/reports/summary/"
    )

    assert response.status_code == 200
    assert response.data["total_entries"] == 10
    assert response.data["total_exits"] == 4
    assert response.data["stock_movements"] == 2
    
    
#este test verifica que se pueda obtener un resumen de inventario a través del endpoint de la API
@pytest.mark.django_db
def test_inventory_dashboard():
    user = UserFactory()
    product = ProductFactory()

    StockMovementFactory(
        product=product,
        movement_type=StockMovement.MovementType.ENTRY,
        quantity=10,
    )

    StockMovementFactory(
        product=product,
        movement_type=StockMovement.MovementType.EXIT,
        quantity=4,
    )

    StockMovementFactory(
        product=product,
        movement_type=StockMovement.MovementType.ADJUSTMENT,
        quantity=7,
    )

    client = APIClient()
    client.force_authenticate(
        user=user
    )

    response = client.get(
        "/api/inventory/dashboard/"
    )

    assert response.status_code == 200
    assert response.data["entries"] == 10
    assert response.data["exits"] == 4
    assert response.data["adjustments"] == 7
    
    
#este test verifica que se pueda filtrar los movimientos de inventario por producto a través del endpoint de la API
@pytest.mark.django_db
def test_filter_movements_by_product():
    user = UserFactory()
    product = ProductFactory()
    other_product = ProductFactory()

    StockMovementFactory(product=product, quantity=5)
    StockMovementFactory(product=other_product, quantity=10)

    client = APIClient()
    client.force_authenticate(user=user)

    response = client.get(
        "/api/inventory/movements/",
        {"product": product.id},
    )

    assert response.status_code == 200
    assert response.data["count"] == 1
    assert response.data["results"][0]["product"]["id"] == product.id

#este test verifica que se pueda filtrar los movimientos de inventario por tipo de movimiento a través del endpoint de la API
@pytest.mark.django_db
def test_order_movements_by_quantity():
    user = UserFactory()
    product = ProductFactory()

    StockMovementFactory(
        product=product,
        quantity=5,
    )

    StockMovementFactory(
        product=product,
        quantity=15,
    )

    client = APIClient()
    client.force_authenticate(
        user=user
    )

    response = client.get(
        "/api/inventory/movements/",
        {
            "ordering": "quantity",
        },
    )

    assert response.status_code == 200

    quantities = [
        item["quantity"]
        for item in response.data["results"]
    ]

    assert quantities == [5, 15]

#este test verifica que se pueda obtener un queryset vacío al utilizar la vista de reportes de inventario con la opción swagger_fake_view activadac   
@pytest.mark.django_db
def test_inventory_report_swagger_fake_view():
    view = InventoryReportView()
    view.swagger_fake_view = True

    queryset = view.get_queryset()

    assert queryset.count() == 0


#este test verifica que se obtenga un error de validación al intentar validar una cantidad inválida en el serializer de movimientos de inventario
@pytest.mark.django_db
def test_stock_movement_serializer_validate_quantity_invalid():
    serializer = StockMovementSerializer()

    with pytest.raises(ValidationError):
        serializer.validate_quantity(0)

import pytest
from rest_framework.test import APIRequestFactory
from inventory.models import StockMovement
from inventory.serializers import StockMovementSerializer
from products.tests.factories import ProductFactory, UserFactory


@pytest.mark.django_db
def test_stock_movement_serializer_representation():
    product = ProductFactory(name="Harina")
    user = UserFactory(email="gabriel@test.com")

    movement = StockMovement.objects.create(
        product=product,
        movement_type=StockMovement.MovementType.ENTRY,
        quantity=5,
        reason="Compra",
        created_by=user,
    )

    serializer = StockMovementSerializer(movement)

    assert serializer.data["product"] == product.id
    assert serializer.data["product_name"] == "Harina"
    assert serializer.data["created_by_email"] == "gabriel@test.com"
    assert serializer.data["quantity"] == 5
    
    

@pytest.mark.django_db
def test_stock_movement_serializer_create():
    product = ProductFactory(stock=10)
    user = UserFactory()

    request = APIRequestFactory().post("/api/inventory/movements/")
    request.user = user

    serializer = StockMovementSerializer(
        context={"request": request}
    )

    movement = serializer.create({
        "product": product,
        "movement_type": StockMovement.MovementType.ENTRY,
        "quantity": 5,
        "reason": "Compra",
    })

    movement.refresh_from_db()
    product.refresh_from_db()

    assert movement.created_by == user
    assert movement.product == product
    assert movement.quantity == 5
    assert product.stock == 15
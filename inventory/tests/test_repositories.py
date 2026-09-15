import pytest

from inventory.models import StockMovement
from inventory.repositories import StockMovementRepository
from products.tests.factories import ProductFactory, UserFactory


@pytest.mark.django_db
def test_get_all_returns_all_movements():
    product = ProductFactory()
    user = UserFactory()

    StockMovementRepository.create(
        product=product,
        movement_type=StockMovement.MovementType.ENTRY,
        quantity=5,
        reason="Compra",
        created_by=user,
    )

    StockMovementRepository.create(
        product=product,
        movement_type=StockMovement.MovementType.EXIT,
        quantity=2,
        reason="Venta",
        created_by=user,
    )

    movements = StockMovementRepository.get_all()

    assert movements.count() == 2


@pytest.mark.django_db
def test_get_by_product_returns_only_product_movements():
    product1 = ProductFactory()
    product2 = ProductFactory()
    user = UserFactory()

    StockMovementRepository.create(
        product=product1,
        movement_type=StockMovement.MovementType.ENTRY,
        quantity=5,
        created_by=user,
    )

    StockMovementRepository.create(
        product=product2,
        movement_type=StockMovement.MovementType.ENTRY,
        quantity=10,
        created_by=user,
    )

    movements = StockMovementRepository.get_by_product(product1.id)

    assert movements.count() == 1
    assert movements.first().product_id == product1.id
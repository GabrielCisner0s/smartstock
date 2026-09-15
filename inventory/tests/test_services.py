import pytest
from inventory.selectors import InventorySelector
from rest_framework.exceptions import ValidationError

from inventory.models import StockMovement
from inventory.services import (
    InventoryService,
    InventoryReportService,
)
from inventory.tests.factories import StockMovementFactory
from products.tests.factories import ProductFactory, UserFactory


@pytest.mark.django_db
def test_register_entry_increases_stock():
    product = ProductFactory(stock=10)
    user = UserFactory()

    movement = InventoryService.register_movement(
        {
            "product": product,
            "movement_type": StockMovement.MovementType.ENTRY,
            "quantity": 5,
            "reason": "Compra de mercadería",
            "created_by": user,
        }
    )

    product.refresh_from_db()

    assert product.stock == 15
    assert movement.product == product
    assert movement.movement_type == StockMovement.MovementType.ENTRY
    assert movement.quantity == 5
    assert movement.created_by == user


@pytest.mark.django_db
def test_register_exit_decreases_stock():
    product = ProductFactory(stock=10)
    user = UserFactory()

    movement = InventoryService.register_movement(
        {
            "product": product,
            "movement_type": StockMovement.MovementType.EXIT,
            "quantity": 4,
            "reason": "Venta",
            "created_by": user,
        }
    )

    product.refresh_from_db()

    assert product.stock == 6
    assert movement.product == product
    assert movement.movement_type == StockMovement.MovementType.EXIT
    assert movement.quantity == 4
    assert movement.created_by == user


@pytest.mark.django_db
def test_register_adjustment_replaces_stock():
    product = ProductFactory(stock=10)
    user = UserFactory()

    movement = InventoryService.register_movement(
        {
            "product": product,
            "movement_type": StockMovement.MovementType.ADJUSTMENT,
            "quantity": 25,
            "reason": "Ajuste de inventario",
            "created_by": user,
        }
    )

    product.refresh_from_db()

    assert product.stock == 25
    assert movement.product == product
    assert movement.movement_type == StockMovement.MovementType.ADJUSTMENT
    assert movement.quantity == 25
    assert movement.created_by == user


@pytest.mark.django_db
def test_register_movement_rejects_zero_quantity():
    product = ProductFactory(stock=10)
    user = UserFactory()

    with pytest.raises(
        ValidationError,
        match="La cantidad debe ser mayor a cero.",
    ):
        InventoryService.register_movement(
            {
                "product": product,
                "movement_type": StockMovement.MovementType.ENTRY,
                "quantity": 0,
                "reason": "Cantidad inválida",
                "created_by": user,
            }
        )


@pytest.mark.django_db
def test_register_movement_rejects_negative_quantity():
    product = ProductFactory(stock=10)
    user = UserFactory()

    with pytest.raises(
        ValidationError,
        match="La cantidad debe ser mayor a cero.",
    ):
        InventoryService.register_movement(
            {
                "product": product,
                "movement_type": StockMovement.MovementType.ENTRY,
                "quantity": -5,
                "reason": "Cantidad inválida",
                "created_by": user,
            }
        )


@pytest.mark.django_db
def test_register_exit_rejects_insufficient_stock():
    product = ProductFactory(stock=5)
    user = UserFactory()

    with pytest.raises(
        ValidationError,
        match="Stock insuficiente",
    ):
        InventoryService.register_movement(
            {
                "product": product,
                "movement_type": StockMovement.MovementType.EXIT,
                "quantity": 10,
                "reason": "Salida superior al stock",
                "created_by": user,
            }
        )


@pytest.mark.django_db
def test_register_movement_rejects_nonexistent_product():
    product = ProductFactory()
    user = UserFactory()

    product_id = product.pk
    product.delete()

    with pytest.raises(
        ValidationError,
        match="El producto no existe.",
    ):
        InventoryService.register_movement(
            {
                "product": product,
                "movement_type": StockMovement.MovementType.ENTRY,
                "quantity": 5,
                "reason": "Producto inexistente",
                "created_by": user,
            }
        )

@pytest.mark.django_db
def test_inventory_report_summary():
    product = ProductFactory(stock=10)
    user = UserFactory()

    InventoryService.register_movement(
        {
            "product": product,
            "movement_type": StockMovement.MovementType.ENTRY,
            "quantity": 5,
            "reason": "Entrada",
            "created_by": user,
        }
    )

    InventoryService.register_movement(
        {
            "product": product,
            "movement_type": StockMovement.MovementType.EXIT,
            "quantity": 2,
            "reason": "Salida",
            "created_by": user,
        }
    )

    result = InventoryReportService.summary()

    assert result["total_entries"] == 5
    assert result["total_exits"] == 2
    assert result["stock_movements"] == 2
    
    
    
@pytest.mark.django_db
def test_inventory_movements_report():
    product = ProductFactory()
    user = UserFactory()

    movement = InventoryService.register_movement(
        {
            "product": product,
            "movement_type": StockMovement.MovementType.ENTRY,
            "quantity": 5,
            "reason": "Entrada",
            "created_by": user,
        }
    )

    result = InventoryReportService.movements_report(
        movement.created_at,
        movement.created_at,
    )

    assert result is not None

#este test verifica que se pueda obtener un resumen de inventario a través del endpoint de la API
@pytest.mark.django_db
def test_stock_movement_str():
    product = ProductFactory(name="Harina")
    user = UserFactory()

    movement = StockMovement.objects.create(
        product=product,
        movement_type=StockMovement.MovementType.ENTRY,
        quantity=5,
        created_by=user,
    )

    assert str(movement) == "Harina - ENTRY"



@pytest.mark.django_db
def test_inventory_report_summary_returns_zero_when_no_entries_or_exits(
    monkeypatch,
):
    monkeypatch.setattr(
        InventorySelector,
        "total_entries",
        lambda: {"total": None},
    )

    monkeypatch.setattr(
        InventorySelector,
        "total_exits",
        lambda: {"total": None},
    )

    result = InventoryReportService.summary()

    assert result["total_entries"] == 0
    assert result["total_exits"] == 0
    assert result["stock_movements"] == 0
    


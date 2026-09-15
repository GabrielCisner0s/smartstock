import pytest

from inventory.models import StockMovement
from inventory.selectors import (
    InventorySelector,
    StockMovementSelector,
    InventoryDashboardSelector,
)
from inventory.tests.factories import StockMovementFactory
from products.tests.factories import ProductFactory


@pytest.mark.django_db
def test_movements_between_returns_movements_in_date_range():
    movement = StockMovementFactory()

    result = InventorySelector.movements_between(
        movement.created_at.date(),
        movement.created_at.date(),
    )

    assert movement in result


@pytest.mark.django_db
def test_movements_between_returns_empty_queryset_when_no_movements():
    StockMovementFactory()

    result = InventorySelector.movements_between(
        "2020-01-01",
        "2020-01-02",
    )

    assert result.count() == 0


@pytest.mark.django_db
def test_total_entries_returns_sum_of_entry_movements():
    product = ProductFactory()

    StockMovementFactory(
        product=product,
        movement_type=StockMovement.MovementType.ENTRY,
        quantity=5,
    )

    StockMovementFactory(
        product=product,
        movement_type=StockMovement.MovementType.ENTRY,
        quantity=7,
    )

    StockMovementFactory(
        product=product,
        movement_type=StockMovement.MovementType.EXIT,
        quantity=20,
    )

    result = InventorySelector.total_entries()

    assert result["total"] == 12


@pytest.mark.django_db
def test_total_exits_returns_sum_of_exit_movements():
    product = ProductFactory()

    StockMovementFactory(
        product=product,
        movement_type=StockMovement.MovementType.EXIT,
        quantity=4,
    )

    StockMovementFactory(
        product=product,
        movement_type=StockMovement.MovementType.EXIT,
        quantity=6,
    )

    StockMovementFactory(
        product=product,
        movement_type=StockMovement.MovementType.ENTRY,
        quantity=50,
    )

    result = InventorySelector.total_exits()

    assert result["total"] == 10


@pytest.mark.django_db
def test_total_entries_returns_none_when_no_entries():
    result = InventorySelector.total_entries()

    assert result["total"] is None


@pytest.mark.django_db
def test_total_exits_returns_none_when_no_exits():
    result = InventorySelector.total_exits()

    assert result["total"] is None


@pytest.mark.django_db
def test_stock_movement_selector_movements_returns_all_movements():
    movement = StockMovementFactory()

    result = StockMovementSelector.movements()

    assert movement in result


@pytest.mark.django_db
def test_stock_movement_selector_get_all_returns_all_movements():
    movement = StockMovementFactory()

    result = StockMovementSelector.get_all()

    assert movement in result


@pytest.mark.django_db
def test_stock_movement_selector_by_product():
    product_1 = ProductFactory()
    product_2 = ProductFactory()

    movement_1 = StockMovementFactory(
        product=product_1,
    )

    movement_2 = StockMovementFactory(
        product=product_2,
    )

    result = StockMovementSelector.by_product(
        product_1.pk
    )

    assert movement_1 in result
    assert movement_2 not in result


@pytest.mark.django_db
def test_stock_movement_selector_by_type():
    product = ProductFactory()

    entry = StockMovementFactory(
        product=product,
        movement_type=StockMovement.MovementType.ENTRY,
    )

    exit_movement = StockMovementFactory(
        product=product,
        movement_type=StockMovement.MovementType.EXIT,
    )

    result = StockMovementSelector.by_type(
        StockMovement.MovementType.ENTRY
    )

    assert entry in result
    assert exit_movement not in result


@pytest.mark.django_db
def test_inventory_dashboard_summary():
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
        quantity=20,
    )

    result = InventoryDashboardSelector.summary()

    assert result["entries"] == 10
    assert result["exits"] == 4
    assert result["adjustments"] == 20


@pytest.mark.django_db
def test_inventory_dashboard_summary_returns_zero_when_empty():
    result = InventoryDashboardSelector.summary()

    assert result["entries"] == 0
    assert result["exits"] == 0
    assert result["adjustments"] == 0
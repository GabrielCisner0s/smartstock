import pytest
from rest_framework.exceptions import ValidationError
from inventory.validators import InventoryValidator
from products.tests.factories import ProductFactory


@pytest.mark.django_db
def test_stock_insuficiente():

    product = ProductFactory(
        stock=5
    )


    with pytest.raises(
        ValidationError
    ):

        InventoryValidator.validate_stock(
            product,
            10
        )

#este test verifica que se pueda obtener un resumen de inventario a través del endpoint de la API
@pytest.mark.parametrize("quantity", [0, -1])
def test_validate_quantity_invalid(quantity):
    with pytest.raises(ValidationError) as exc_info:
        InventoryValidator.validate_quantity(quantity)

    assert exc_info.value.detail["quantity"] == (
        "La cantidad debe ser mayor a cero."
    )
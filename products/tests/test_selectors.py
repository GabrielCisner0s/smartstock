import pytest

from inventory.models import StockMovement
from products.models import Product
from products.selectors import ProductSelector
from products.tests.factories import (
    CategoryFactory,
    ProductFactory,
    UserFactory,
)

#este test verifica que la función get_all devuelva solo los productos que no están marcados como eliminados
@pytest.mark.django_db
def test_get_all_returns_only_non_deleted_products():
    active_product = ProductFactory()
    ProductFactory(is_deleted=True)

    products = ProductSelector.get_all()

    assert list(products) == [active_product]


@pytest.mark.django_db
def test_active_products_returns_non_deleted_products():
    product = ProductFactory()

    products = ProductSelector.active_products()

    assert product in products


@pytest.mark.django_db
def test_low_stock_returns_products_below_minimum():
    low_stock_product = ProductFactory(
        stock=2,
        minimum_stock=5,
    )

    normal_product = ProductFactory(
        stock=10,
        minimum_stock=5,
    )

    products = ProductSelector.low_stock()

    assert low_stock_product in products
    assert normal_product not in products


@pytest.mark.django_db
def test_out_of_stock_returns_products_with_zero_stock():
    out_product = ProductFactory(stock=0)
    available_product = ProductFactory(stock=10)

    products = ProductSelector.out_of_stock()

    assert out_product in products
    assert available_product not in products


@pytest.mark.django_db
def test_most_moved_orders_products_by_exit_quantity():
    user = UserFactory()

    product1 = ProductFactory()
    product2 = ProductFactory()

    StockMovement.objects.create(
        product=product1,
        movement_type=StockMovement.MovementType.EXIT,
        quantity=3,
        created_by=user,
    )

    StockMovement.objects.create(
        product=product2,
        movement_type=StockMovement.MovementType.EXIT,
        quantity=10,
        created_by=user,
    )

    products = list(ProductSelector.most_moved())

    assert products[0] == product2
    assert products[1] == product1


@pytest.mark.django_db
def test_base_queryset_excludes_deleted_products():
    product = ProductFactory()
    ProductFactory(is_deleted=True)

    products = ProductSelector.base_queryset()

    assert product in products
    assert products.count() == 1


@pytest.mark.django_db
def test_active_returns_only_active_products():
    active_product = ProductFactory(
        status=Product.Status.ACTIVE
    )

    inactive_product = ProductFactory(
        status=Product.Status.INACTIVE
    )

    products = ProductSelector.active()

    assert active_product in products
    assert inactive_product not in products

#este test verifica que la función de búsqueda por categoría devuelva los productos correctos y no incluya productos de otras categorías
@pytest.mark.django_db
def test_inactive_returns_only_inactive_products():
    inactive_product = ProductFactory(
        status=Product.Status.INACTIVE
    )

    active_product = ProductFactory(
        status=Product.Status.ACTIVE
    )

    products = ProductSelector.inactive()

    assert inactive_product in products
    assert active_product not in products

#este test verifica que la función de búsqueda por categoría devuelva los productos correctos y no incluya productos de otras categorías
@pytest.mark.django_db
def test_by_category_returns_products_of_category():
    category1 = CategoryFactory()
    category2 = CategoryFactory()

    product1 = ProductFactory(category=category1)
    product2 = ProductFactory(category=category2)

    products = ProductSelector.by_category(category1.id)

    assert product1 in products
    assert product2 not in products

#este test verifica que la función de búsqueda por nombre devuelva el producto correcto y no incluya otros productos
@pytest.mark.django_db
def test_search_by_name():
    matching_product = ProductFactory(
        name="Teclado Mecánico"
    )

    other_product = ProductFactory(
        name="Monitor"
    )

    products = ProductSelector.search("teclado")

    assert matching_product in products
    assert other_product not in products


#este test verifica que la función de búsqueda por SKU devuelva el producto correcto y no incluya otros productos
@pytest.mark.django_db
def test_search_by_sku():
    matching_product = ProductFactory(
        sku="TEC-001"
    )

    other_product = ProductFactory(
        sku="MON-001"
    )

    products = ProductSelector.search("TEC-001")

    assert matching_product in products
    assert other_product not in products
    
import pytest

from products.models import Category, Product
from products.tests.factories import CategoryFactory, ProductFactory


@pytest.mark.django_db
def test_category_str_returns_name():
    category = CategoryFactory(name="Electrónica")

    assert str(category) == "Electrónica"


@pytest.mark.django_db
def test_product_str_returns_name():
    product = ProductFactory(name="Teclado Mecánico")

    assert str(product) == "Teclado Mecánico"
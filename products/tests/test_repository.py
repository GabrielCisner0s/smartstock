import pytest

from products.repositories import ProductRepository
from products.tests.factories import ProductFactory


@pytest.mark.django_db
def test_repository_get_all():

    ProductFactory.create_batch(3)

    products = ProductRepository.get_all()

    assert products.count() == 3


@pytest.mark.django_db
def test_repository_get_by_id():

    product = ProductFactory()

    result = ProductRepository.get_by_id(product.id)

    assert result.id == product.id
    
@pytest.mark.django_db
def test_get_by_sku():
    product = ProductFactory(sku="SKU-001")

    result = ProductRepository.get_by_sku("SKU-001")

    assert result == product
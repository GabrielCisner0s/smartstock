import pytest

from products.filters import ProductFilter
from products.models import Product
from products.tests.factories import ProductFactory


@pytest.mark.django_db
def test_filter_products_by_minimum_price():

    ProductFactory(price=1000)
    ProductFactory(price=5000)
    ProductFactory(price=10000)

    filter_set = ProductFilter(
        data={
            "price_min": 5000
        },
        queryset=ProductFactory._meta.model.objects.all()
    )
    assert filter_set.qs.count() == 2


@pytest.mark.django_db
def test_filter_products_by_maximum_price():

    ProductFactory(price=1000)
    ProductFactory(price=5000)
    ProductFactory(price=10000)

    filter_set = ProductFilter(
        data={
            "price_max": 5000
        },
        queryset=Product.objects.all()
    )

    assert filter_set.qs.count() == 2


@pytest.mark.django_db
def test_filter_products_by_price_range():

    ProductFactory(price=1000)
    ProductFactory(price=5000)
    ProductFactory(price=10000)

    filter_set = ProductFilter(
        data={
            "price_min": 2000,
            "price_max": 6000,
        },
        queryset=Product.objects.all()
    )

    assert filter_set.qs.count() == 1


@pytest.mark.django_db
def test_filter_products_by_minimum_stock():

    ProductFactory(stock=5)
    ProductFactory(stock=20)
    ProductFactory(stock=50)

    filter_set = ProductFilter(
        data={
            "stock_min": 20
        },
        queryset=Product.objects.all()
    )

    assert filter_set.qs.count() == 2


@pytest.mark.django_db
def test_filter_products_by_maximum_stock():

    ProductFactory(stock=5)
    ProductFactory(stock=20)
    ProductFactory(stock=50)

    filter_set = ProductFilter(
        data={
            "stock_max": 20
        },
        queryset=Product.objects.all()
    )

    assert filter_set.qs.count() == 2
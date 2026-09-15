import pytest

from rest_framework.exceptions import ValidationError

from products.validators import ProductValidator


def test_price_cannot_be_zero():

    with pytest.raises(ValidationError):

        ProductValidator.validate_price(0)


def test_stock_cannot_be_negative():

    with pytest.raises(ValidationError):

        ProductValidator.validate_stock(-5)
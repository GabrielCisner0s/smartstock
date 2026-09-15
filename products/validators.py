from rest_framework.exceptions import ValidationError




class ProductValidator:

    @staticmethod
    def validate_price(price):

        if price <= 0:
            raise ValidationError({
                "price": "El precio debe ser mayor que cero."
            })

    @staticmethod
    def validate_stock(stock):

        if stock < 0:
            raise ValidationError({
                "stock": "El stock no puede ser negativo."
            })
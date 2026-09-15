from rest_framework.exceptions import ValidationError


class InventoryValidator:


    @staticmethod
    def validate_quantity(quantity):

        if quantity <= 0:
            raise ValidationError({
                "quantity": (
                    "La cantidad debe ser mayor a cero."
                )
            })


    @staticmethod
    def validate_stock(product, quantity):

        if product.stock < quantity:

            raise ValidationError({
                "quantity": (
                    f"Stock insuficiente. "
                    f"Disponible: {product.stock}"
                )
            })
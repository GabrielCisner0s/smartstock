from django.db import transaction
from rest_framework.exceptions import ValidationError

from inventory.selectors import InventorySelector
from products.models import Product
    
from .models import StockMovement
from .repositories import StockMovementRepository
from .validators import InventoryValidator


class InventoryService:


    @staticmethod
    @transaction.atomic
    def register_movement(data):

        try:

            product = (
                Product.objects
                .select_for_update()
                .get(
                    id=data["product"].pk,
                    is_deleted=False
                )
            )

        except Product.DoesNotExist:

            raise ValidationError(
                "El producto no existe."
            )


        movement_type = data["movement_type"]
        quantity = data["quantity"]


        if quantity <= 0:

            raise ValidationError(
                "La cantidad debe ser mayor a cero."
            )


        if movement_type == StockMovement.MovementType.EXIT:

            InventoryValidator.validate_stock(
                product,
                quantity
            )

            product.stock -= quantity


        elif movement_type == StockMovement.MovementType.ENTRY:

            product.stock += quantity


        elif movement_type == StockMovement.MovementType.ADJUSTMENT:

            product.stock = quantity


        product.save(
            update_fields=[
                "stock"
            ]
        )


        movement = (
            StockMovementRepository.create(
                **data
            )
        )


        return movement 
    
class InventoryReportService:

    @staticmethod
    def summary():

        total_entries = (
            InventorySelector.total_entries()["total"] or 0
        )

        total_exits = (
            InventorySelector.total_exits()["total"] or 0
        )

        total_movements = (
            StockMovement.objects.count()
        )

        return {
            "total_entries": total_entries,
            "total_exits": total_exits,
            "stock_movements": total_movements,
        }
        
    @staticmethod
    def movements_report(start, end):

        return InventorySelector.movements_between(
            start,
            end,
        )
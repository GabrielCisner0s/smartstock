from django.db.models import Sum

from inventory.models import StockMovement


class InventorySelector:

    @staticmethod
    def movements_between(start, end):

        return (
            StockMovement.objects
            .filter(
                created_at__date__range=(
                    start,
                    end,
                )
            )
            .select_related(
                "product",
                "created_by",
            )
        )

    @staticmethod
    def total_entries():

        return (
            StockMovement.objects
            .filter(
                movement_type=StockMovement.MovementType.ENTRY
            )
            .aggregate(
                total=Sum("quantity")
            )
        )

    @staticmethod
    def total_exits():

        return (
            StockMovement.objects
            .filter(
                movement_type=StockMovement.MovementType.EXIT
            )
            .aggregate(
                total=Sum("quantity")
            )
        )
        

class StockMovementSelector:

    @staticmethod
    def movements():
        return (
            StockMovement.objects
            .select_related(
                "product",
                "created_by",
            )
        )
        
    
    @staticmethod
    def get_all():
        return (
            StockMovement.objects
            .select_related(
                "product",
                "created_by",
            )
        )


    @staticmethod
    def by_product(product_id):

        return (
            StockMovement.objects
            .filter(
                product_id=product_id
            )
            .select_related(
                "product",
                "created_by",
            )
        )


    @staticmethod
    def by_type(movement_type):

        return (
            StockMovement.objects
            .filter(
                movement_type=movement_type
            )
            .select_related(
                "product",
                "created_by",
            )
        )
        
class InventoryDashboardSelector:

    @staticmethod
    def summary():

        entries = (
            StockMovement.objects
            .filter(
                movement_type=StockMovement.MovementType.ENTRY
            )
            .aggregate(total=Sum("quantity"))
        )

        exits = (
            StockMovement.objects
            .filter(
                movement_type=StockMovement.MovementType.EXIT
            )
            .aggregate(total=Sum("quantity"))
        )

        adjustments = (
            StockMovement.objects
            .filter(
                movement_type=StockMovement.MovementType.ADJUSTMENT
            )
            .aggregate(total=Sum("quantity"))
        )

        return {
            "entries": entries["total"] or 0,
            "exits": exits["total"] or 0,
            "adjustments": adjustments["total"] or 0,
        }
from .models import StockMovement


class StockMovementRepository:


    @staticmethod
    def create(**data):

        return StockMovement.objects.create(
            **data
        )


    @staticmethod
    def get_all():

        return (
            StockMovement.objects
            .select_related(
                "product",
                "created_by"
            )
        )


    @staticmethod
    def get_by_product(product_id):

        return (
            StockMovement.objects
            .select_related(
                "product",
                "created_by"
            )
            .filter(
                product_id=product_id
            )
        )
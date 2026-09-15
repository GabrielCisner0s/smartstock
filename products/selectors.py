from inventory.models import StockMovement
from django.db.models import (
    F,
    Sum,
    Q,
)


from products.models import Product


class ProductSelector:

    @staticmethod
    def get_all():
        return (
            Product.objects
            .filter(is_deleted=False)
            .select_related("category")
        )

    @staticmethod
    def active_products():
        return ProductSelector.get_all()

    @staticmethod
    def low_stock():
        return (
            Product.objects
            .filter(
                stock__lte=F("minimum_stock"),
                is_deleted=False,
            )
            .select_related("category")
        )

    @staticmethod
    def out_of_stock():
        return (
            Product.objects
            .filter(
                stock=0,
                is_deleted=False,
            )
        )
    
    @staticmethod
    def most_moved():

        return (
            Product.objects
            .filter(is_deleted=False)
            .annotate(
                total_exits=Sum(
                    "movements__quantity",
                    filter=Q(
                        movements__movement_type=StockMovement.MovementType.EXIT
                    )
                )
            )
            .order_by("-total_exits")
        )
        
    @staticmethod
    def base_queryset():
        return (
            Product.objects
            .filter(is_deleted=False)
            .select_related("category")
    )

    @staticmethod
    def active():
        return (
            ProductSelector.base_queryset()
            .filter(status=Product.Status.ACTIVE)
    )
        
    @staticmethod
    def inactive():
        return (
            ProductSelector.base_queryset()
            .filter(status=Product.Status.INACTIVE)
    )
        
        
    @staticmethod
    def by_category(category_id):
        return (
            ProductSelector.base_queryset()
            .filter(category_id=category_id)
    )
        

    @staticmethod
    def search(query):
        return (
            ProductSelector.base_queryset()
            .filter(
                Q(name__icontains=query) |
                Q(sku__icontains=query)
            )
    )

    
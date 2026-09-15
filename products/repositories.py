from .models import Product


class ProductRepository:

    @staticmethod
    def get_all():
        return (
            Product.objects
            .filter(is_deleted=False)
            .select_related("category")
        )

    @staticmethod
    def get_by_id(product_id):
        return (
            Product.objects
            .filter(is_deleted=False)
            .select_related("category")
            .get(id=product_id)
        )

    @staticmethod
    def get_by_sku(sku):
        return (
            Product.objects
            .filter(is_deleted=False)
            .get(sku=sku)
        )

    @staticmethod
    def exists_by_sku(sku):
        return (
            Product.objects
            .filter(is_deleted=False, sku=sku)
            .exists()
        )

    @staticmethod
    def create(**data):
        return Product.objects.create(**data)

    @staticmethod
    def update(product, **data):
        for field, value in data.items():
            setattr(product, field, value)

        product.save(update_fields=list(data.keys()))

        return product

    @staticmethod
    def delete(product):

        product.is_deleted = True

        product.save(
            update_fields=[
                "is_deleted",
                "updated_by",
            ]
        )

        return product

    @staticmethod
    def restore(product, user):

        product.is_deleted = False
        product.updated_by = user

        product.save(
            update_fields=[
                "is_deleted",
                "updated_by",
            ]
        )

        return product
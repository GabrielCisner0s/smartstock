from django.db import transaction
from rest_framework.exceptions import ValidationError

from .models import Category
from .repositories import ProductRepository
from .validators import ProductValidator

class CategoryService:

    @staticmethod
    @transaction.atomic
    def create_category(data):

        name = data["name"]

        if Category.objects.filter(name=name).exists():
            raise ValidationError({
                "name": "La categoría ya existe."
            })

        return Category.objects.create(**data)



#esta clase es la que se encarga de la logica de negocio de los productos, es decir, las validaciones y reglas de negocio que se deben cumplir antes de crear, actualizar o eliminar un producto.
class ProductService:

    @staticmethod
    @transaction.atomic
    def create_product(validated_data, user):
        
        # Validar los datos del producto
        ProductValidator.validate_price(validated_data["price"])
        ProductValidator.validate_stock(validated_data["stock"])

        if ProductRepository.exists_by_sku(validated_data["sku"]):
            raise ValidationError({
                "sku": "Ya existe un producto con ese SKU."
            })

        validated_data["created_by"] = user

        return ProductRepository.create(
            **validated_data
        )
                
            
    
    
    @staticmethod
    @transaction.atomic
    def update_product(product, validated_data, user):

        if "price" in validated_data:
            ProductValidator.validate_price(
                validated_data["price"]
            )

        if "stock" in validated_data:
            ProductValidator.validate_stock(
                validated_data["stock"]
            )

        sku = validated_data.get("sku")

        if sku and sku != product.sku:
            if ProductRepository.exists_by_sku(sku):
                raise ValidationError({
                    "sku": "Ya existe un producto con ese SKU."
                })

         # created_by es inmutable
        validated_data.pop("created_by", None)
        
        validated_data["updated_by"] = user

        return ProductRepository.update(
            product,
            **validated_data
        )


    @staticmethod
    @transaction.atomic
    def delete_product(product, user):

        product.updated_by = user

        return ProductRepository.delete(
            product
        )


    @staticmethod
    @transaction.atomic
    def restore_product(product, user):

        return ProductRepository.restore(
            product,
            user
        )
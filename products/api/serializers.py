from rest_framework import serializers

from products.models import Product, Category
from products.services import ProductService

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = (
            "id",
            "name",
            "description",
            "created_at",
        )

        read_only_fields = (
            "id",
            "created_at",
        )

class ProductSerializer(serializers.ModelSerializer):

    category = CategorySerializer(read_only=True)

    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source="category",
        write_only=True
    )
    
    class Meta:
        model = Product

        fields = (
            "id",
            "sku",
            "name",
            "description",
            "category",
            "category_id",
            "price",
            "stock",
            "minimum_stock",
            "status",
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )
    
    def create(self, validated_data):

        user = self.context["request"].user

        return ProductService.create_product(
            validated_data,
            user,
        )


    def update(self, instance, validated_data):
        user = self.context["request"].user

        return ProductService.update_product(
            instance,
            validated_data,
            user,
        )
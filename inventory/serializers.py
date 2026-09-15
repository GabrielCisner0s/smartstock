from rest_framework import serializers
from products.models import Product
from .models import StockMovement
from .services import InventoryService


class StockMovementSerializer(serializers.ModelSerializer):

    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.filter(
            is_deleted=False
    )
)
    
    product_name = serializers.CharField(
        source="product.name",
        read_only=True
    )

    created_by_email = serializers.CharField(
        source="created_by.email",
        read_only=True
    )


    class Meta:

        model = StockMovement

        fields = (
            "id",
            "product",
            "product_name",
            "movement_type",
            "quantity",
            "reason",
            "created_by",
            "created_by_email",
            "created_at",
        )


        read_only_fields = (
            "id",
            "created_by",
            "created_at",
            "product_name",
            "created_by_email",
        )


    def create(self, validated_data):

        user = self.context["request"].user

        validated_data["created_by"] = user

        return InventoryService.register_movement(
            validated_data
        )
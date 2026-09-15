from django.contrib.auth import get_user_model
from rest_framework import serializers

from inventory.models import StockMovement
from inventory.services import InventoryService
from products.models import Product


User = get_user_model()


class ProductSimpleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = (
            "id",
            "sku",
            "name",
        )


class UserSimpleSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "role",
        )


class StockMovementSerializer(serializers.ModelSerializer):

    product = ProductSimpleSerializer(
        read_only=True
    )

    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.filter(
            is_deleted=False
        ),
        source="product",
        write_only=True,
    )

    created_by = UserSimpleSerializer(
        read_only=True
    )


    class Meta:

        model = StockMovement

        fields = (
            "id",
            "product",
            "product_id",
            "movement_type",
            "quantity",
            "reason",
            "created_by",
            "created_at",
        )

        read_only_fields = (
            "id",
            "created_at",
            "created_by",
        )


    def validate_quantity(self, value):

        if value <= 0:
            raise serializers.ValidationError(
                "La cantidad debe ser mayor a cero."
            )

        return value


    def create(self, validated_data):

        request = self.context.get(
            "request"
        )

        if request and request.user.is_authenticated:
            validated_data["created_by"] = request.user


        return InventoryService.register_movement(
            validated_data
        )
        
class InventorySummarySerializer(
    serializers.Serializer
):

    total_products = serializers.IntegerField()
    total_stock = serializers.IntegerField()
    low_stock = serializers.IntegerField()
    out_of_stock = serializers.IntegerField()  


class InventoryDashboardSerializer(serializers.Serializer):

    entries = serializers.IntegerField()
    exits = serializers.IntegerField()
    adjustments = serializers.IntegerField()
    


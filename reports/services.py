from django.db.models import Count
from django.utils import timezone

from inventory.models import StockMovement
from products.models import Product


class DashboardService:

    @staticmethod
    def get_summary():

        today = timezone.now().date()

        return {
            "total_products": Product.objects.filter(
                is_deleted=False
            ).count(),

            "low_stock_products": Product.objects.filter(
                stock__lte=0
            ).count(),

            "active_products": Product.objects.filter(
                is_deleted=False,
                status=Product.Status.ACTIVE,
            ).count(),

            "entries_today": StockMovement.objects.filter(
                movement_type=StockMovement.MovementType.ENTRY,
                created_at__date=today,
            ).count(),

            "exits_today": StockMovement.objects.filter(
                movement_type=StockMovement.MovementType.EXIT,
                created_at__date=today,
            ).count(),
        }
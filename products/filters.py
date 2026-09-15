import django_filters

from products.models import Product


class ProductFilter(django_filters.FilterSet):

    price_min = django_filters.NumberFilter(
        field_name="price",
        lookup_expr="gte",
    )

    price_max = django_filters.NumberFilter(
        field_name="price",
        lookup_expr="lte",
    )

    stock_min = django_filters.NumberFilter(
        field_name="stock",
        lookup_expr="gte",
    )

    stock_max = django_filters.NumberFilter(
        field_name="stock",
        lookup_expr="lte",
    )

    created_after = django_filters.DateFilter(
        field_name="created_at",
        lookup_expr="date__gte",
    )

    created_before = django_filters.DateFilter(
        field_name="created_at",
        lookup_expr="date__lte",
    )

    category = django_filters.NumberFilter(
        field_name="category_id",
    )

    status = django_filters.CharFilter(
        field_name="status",
    )

    class Meta:
        model = Product
        fields = [
            "category",
            "status",
            "price_min",
            "price_max",
            "stock_min",
            "stock_max",
            "created_after",
            "created_before",
        ]
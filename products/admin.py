from django.contrib import admin

from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "sku",
        "name",
        "category",
        "price",
        "stock",
        "status",
    )

    list_filter = (
        "category",
        "status",
    )

    search_fields = (
        "sku",
        "name",
    )

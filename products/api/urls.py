from django.urls import path

from .views import (
    CategoryListCreateView,
    CategoryDetailView,
    ProductListCreateView,
    ProductDetailView,
    ProductLowStockView,
    ProductRestoreView,
)

urlpatterns = [
    path(
        "categories/",
        CategoryListCreateView.as_view(),
        name="categories"
    ),

    path(
        "categories/<int:pk>/",
        CategoryDetailView.as_view(),
        name="category-detail"
    ),


    path(
        "",
        ProductListCreateView.as_view(),
        name="products"
    ),

    path(
        "<int:pk>/",
        ProductDetailView.as_view(),
        name="product-detail"
    ),
    path(
        "low-stock/",
        ProductLowStockView.as_view(),
        name="product-low-stock"
    ),
    path(
        "<int:pk>/restore/",
        ProductRestoreView.as_view(),
        name="product-restore",
    ),
]

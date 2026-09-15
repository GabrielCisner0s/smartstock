"""
URL configuration for config project.
"""

from django.contrib import admin
from django.urls import include, path

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)


urlpatterns = [

    # ==============================
    # ADMIN
    # ==============================

    path(
        "admin/",
        admin.site.urls,
    ),


    # ==============================
    # DOCUMENTACIÓN API
    # ==============================

    path(
        "api/schema/",
        SpectacularAPIView.as_view(),
        name="schema",
    ),

    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(
            url_name="schema"
        ),
        name="swagger-ui",
    ),

    path(
        "api/redoc/",
        SpectacularRedocView.as_view(
            url_name="schema"
        ),
        name="redoc",
    ),


    # ==============================
    # AUTHENTICATION
    # ==============================

    path(
        "api/auth/",
        include("users.api.urls"),
    ),


    # ==============================
    # PRODUCTS
    # ==============================

    path(
        "api/products/",
        include("products.api.urls"),
    ),


    # ==============================
    # INVENTORY
    # ==============================

    path(
        "api/inventory/",
        include("inventory.api.urls"),
    ),


    # ==============================
    # REPORTS
    # ==============================

    path(
        "api/reports/",
        include("reports.api.urls"),
    ),

]
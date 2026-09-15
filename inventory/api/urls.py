from django.urls import path

from .views import (
    StockMovementListCreateView,
    InventoryDashboardView,
    StockMovementDetailView,
    InventorySummaryView,
    InventoryReportView,
)

#REGISTRO DE ENDPOINTS DE LA API DEL MÓDULO DE INVENTARIO
#Este archivo define las rutas de la API para el módulo de inventario. Se importan las vistas correspondientes y se asignan a las rutas específicas.
urlpatterns = [

    path(
        "movements/",
        StockMovementListCreateView.as_view(),
        name="stock-movement-list-create",
    ),

    path(
        "movements/<int:pk>/",
        StockMovementDetailView.as_view(),
        name="stock-movement-detail",
    ),
    path(
        "reports/summary/",
        InventorySummaryView.as_view(),
        name="inventory-summary",
    ),
    path(
        "reports/",
        InventoryReportView.as_view(),
        name="inventory-report",
    ),
    path(
        "dashboard/",
        InventoryDashboardView.as_view(),
        name="inventory-dashboard",
    ),
]
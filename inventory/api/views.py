from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import ValidationError
from inventory.models import StockMovement
from rest_framework import (
    filters,
    generics,
)

from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (
    extend_schema,
    OpenApiParameter,
    OpenApiResponse,
    OpenApiExample,
)

from inventory.services import InventoryReportService
from inventory.permissions import (
    InventoryPermission,
    InventoryReportPermission,
)
from inventory.selectors import (
    StockMovementSelector,
    InventoryDashboardSelector,
)

from inventory.api.serializers import (
    InventorySummarySerializer,
    InventoryDashboardSerializer,
    StockMovementSerializer,
)


# ==========================================
# STOCK MOVEMENTS
# ==========================================

@extend_schema(
    tags=["Inventory"],
    summary="Listar y registrar movimientos de stock",
    description="""
        Gestiona los movimientos de inventario.

        Permisos:
        - ADMIN: puede consultar y registrar movimientos.
        - SUPERVISOR: puede consultar y registrar movimientos.
        - EMPLOYEE: puede consultar y registrar movimientos.

        Autenticación:
        - Requiere Bearer JWT.
    """,
    parameters=[
        OpenApiParameter(
            name="product",
            type=OpenApiTypes.INT,
            description="Filtra los movimientos por ID de producto.",
        ),
        OpenApiParameter(
            name="movement_type",
            type=OpenApiTypes.STR,
            description=(
                "Filtra por tipo de movimiento: "
                "ENTRY, EXIT o ADJUSTMENT."
            ),
        ),
        OpenApiParameter(
            name="ordering",
            type=OpenApiTypes.STR,
            description=(
                "Ordenamiento. Ejemplos: created_at, "
                "-created_at, quantity, -quantity."
            ),
        ),
    ],
    request=StockMovementSerializer,
    responses={
        200: StockMovementSerializer(many=True),
        201: StockMovementSerializer,
        400: OpenApiResponse(
            description="Datos inválidos o stock insuficiente."
        ),
        401: OpenApiResponse(
            description="Usuario no autenticado."
        ),
        403: OpenApiResponse(
            description="Usuario sin permisos."
        ),
    },
    examples=[
        OpenApiExample(
            "Entrada de stock",
            request_only=True,
            value={
                "product": 1,
                "movement_type": "ENTRY",
                "quantity": 20,
                "reason": "Compra de mercadería",
            },
        ),
        OpenApiExample(
            "Salida de stock",
            request_only=True,
            value={
                "product": 1,
                "movement_type": "EXIT",
                "quantity": 5,
                "reason": "Venta",
            },
        ),
        OpenApiExample(
            "Ajuste de stock",
            request_only=True,
            value={
                "product": 1,
                "movement_type": "ADJUSTMENT",
                "quantity": 15,
                "reason": "Corrección de inventario",
            },
        ),
    ],
)
class StockMovementListCreateView(
    generics.ListCreateAPIView
):

    serializer_class = StockMovementSerializer

    permission_classes = [
        InventoryPermission
    ]

    filter_backends = (
        DjangoFilterBackend,
        filters.OrderingFilter,
    )

    filterset_fields = (
        "product",
        "movement_type",
    )

    ordering_fields = (
        "created_at",
        "quantity",
    )

    ordering = (
        "-created_at",
    )

    def get_queryset(self):

        return StockMovementSelector.get_all()


@extend_schema(
    tags=["Inventory"],
    summary="Obtener movimiento de stock",
    description="""
        Obtiene un movimiento de inventario.

        Permisos:
        - ADMIN: permitido.
        - SUPERVISOR: permitido.
        - EMPLOYEE: permitido.

        Autenticación:
        - Requiere Bearer JWT.
    """,
    responses={
        200: StockMovementSerializer,
        401: OpenApiResponse(
            description="Usuario no autenticado."
        ),
        403: OpenApiResponse(
            description="Usuario sin permisos."
        ),
        404: OpenApiResponse(
            description="Movimiento no encontrado."
        ),
    },
)
class StockMovementDetailView(
    generics.RetrieveAPIView
):

    serializer_class = StockMovementSerializer

    permission_classes = [
        InventoryPermission
    ]

    def get_queryset(self):

        return StockMovementSelector.get_all()


# ==========================================
# SUMMARY
# ==========================================

@extend_schema(
    tags=["Inventory"],
    summary="Resumen del inventario",
    description="""
        Obtiene un resumen general del inventario.

        Permisos:
        - ADMIN: permitido.
        - SUPERVISOR: permitido.
        - EMPLOYEE: permitido.

        Autenticación:
        - Requiere Bearer JWT.
    """,
    responses={
        200: InventorySummarySerializer,
        401: OpenApiResponse(
            description="Usuario no autenticado."
        ),
        403: OpenApiResponse(
            description="Usuario sin permisos."
        ),
    },
)
class InventorySummaryView(
    generics.GenericAPIView
):

    permission_classes = [
        InventoryPermission
    ]

    serializer_class = InventorySummarySerializer

    def get(self, request):

        data = InventoryReportService.summary()

        return Response(data)


# ==========================================
# REPORT
# ==========================================

@extend_schema(
    tags=["Inventory"],
    summary="Reporte de movimientos de inventario",
    description=(
        "Obtiene los movimientos de inventario realizados "
        "entre dos fechas."
    ),
    parameters=[
        OpenApiParameter(
            name="start",
            type=OpenApiTypes.DATE,
            required=True,
            description="Fecha inicial del reporte.",
        ),
        OpenApiParameter(
            name="end",
            type=OpenApiTypes.DATE,
            required=True,
            description="Fecha final del reporte.",
        ),
    ],
    responses={
        200: StockMovementSerializer(many=True),
        400: OpenApiResponse(
            description=(
                "Los parámetros 'start' y 'end' son obligatorios "
                "o tienen un formato inválido."
            )
        ),
        401: OpenApiResponse(
            description="Usuario no autenticado."
        ),
        403: OpenApiResponse(
            description="Usuario sin permisos."
        ),
    },
)
class InventoryReportView(
    generics.ListAPIView
):

    serializer_class = StockMovementSerializer

    permission_classes = [
        InventoryPermission
    ]

    def get_queryset(self):

        if getattr(self, "swagger_fake_view", False):
            return StockMovement.objects.none()

        start = self.request.query_params.get("start")
        end = self.request.query_params.get("end")

        if not start or not end:
            raise ValidationError(
                "Los parámetros 'start' y 'end' son obligatorios."
            )

        return InventoryReportService.movements_report(
            start,
            end,
        )



# ==========================================
# DASHBOARD
# ==========================================
@extend_schema(
    tags=["Inventory"],
    summary="Dashboard de inventario",
    description="""
        Obtiene los indicadores principales del inventario.

        Permisos:
        - ADMIN: permitido.
        - SUPERVISOR: permitido.
        - EMPLOYEE: permitido.

        Autenticación:
        - Requiere Bearer JWT.
    """,
    responses={
        200: InventoryDashboardSerializer,
        401: OpenApiResponse(
            description="Usuario no autenticado."
        ),
        403: OpenApiResponse(
            description="Usuario sin permisos."
        ),
    },
)
class InventoryDashboardView(APIView):

    permission_classes = [
        InventoryPermission
    ]

    def get(self, request):

        data = InventoryDashboardSelector.summary()

        serializer = InventoryDashboardSerializer(data)

        return Response(serializer.data)
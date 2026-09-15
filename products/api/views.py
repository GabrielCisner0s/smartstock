
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.response import Response
from products.models import Category, Product
from products.permissions import ProductPermission, IsAdmin
from products.selectors import ProductSelector
from rest_framework.filters import SearchFilter, OrderingFilter
from .serializers import CategorySerializer, ProductSerializer
from products.filters import ProductFilter
from products.repositories import ProductRepository
from drf_spectacular.types import OpenApiTypes

from drf_spectacular.utils import (
    OpenApiParameter,
    extend_schema,
    OpenApiResponse,
)
from products.services import (
    CategoryService,
    ProductService,
)

@extend_schema(
    tags=["Categories"],
    summary="List and create categories",
    description=(
        "Returns all product categories or creates a new category."
    ),
    responses={
        200: CategorySerializer(many=True),
        201: CategorySerializer,
        400: OpenApiResponse(
            description="Invalid category data."
        ),
        401: OpenApiResponse(
            description="Authentication required."
        ),
        403: OpenApiResponse(
            description="User does not have permission."
        ),
    },
)
class CategoryListCreateView(generics.ListCreateAPIView):

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [ProductPermission]


    def perform_create(self, serializer):
        CategoryService.create_category(
            **serializer.validated_data
        )

#esta clase es para obtener, actualizar y eliminar una categoria
@extend_schema(
    tags=["Categories"],
    summary="Retrieve, update or delete a category",
    description=(
        "Retrieves, updates or deletes an existing product category."
    ),
    responses={
        200: CategorySerializer,
        400: OpenApiResponse(
            description="Invalid category data."
        ),
        401: OpenApiResponse(
            description="Authentication required."
        ),
        403: OpenApiResponse(
            description="User does not have permission."
        ),
        404: OpenApiResponse(
            description="Category not found."
        ),
    },
)
class CategoryDetailView(
    generics.RetrieveUpdateDestroyAPIView
):

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [ProductPermission]

#clase para listar y crear productos
@extend_schema(
    tags=["Products"],
    summary="Listar productos",
    description="""
        Lista los productos disponibles.

        Permisos:
        - ADMIN: acceso completo.
        - SUPERVISOR: acceso de lectura.
        - EMPLOYEE: acceso de lectura.

        Requiere autenticación mediante JWT.
    """,
    parameters=[
        OpenApiParameter(
            name="search",
            type=OpenApiTypes.STR,
            description="Busca por SKU, nombre o descripción.",
        ),
        OpenApiParameter(
            name="category",
            type=OpenApiTypes.INT,
            description="Filtra por ID de categoría.",
        ),
        OpenApiParameter(
            name="price_min",
            type=OpenApiTypes.NUMBER,
            description="Precio mínimo.",
        ),
        OpenApiParameter(
            name="price_max",
            type=OpenApiTypes.NUMBER,
            description="Precio máximo.",
        ),
        OpenApiParameter(
            name="stock_min",
            type=OpenApiTypes.INT,
            description="Stock mínimo.",
        ),
        OpenApiParameter(
            name="stock_max",
            type=OpenApiTypes.INT,
            description="Stock máximo.",
        ),
        OpenApiParameter(
            name="created_after",
            type=OpenApiTypes.DATE,
            description="Productos creados después de esta fecha.",
        ),
        OpenApiParameter(
            name="created_before",
            type=OpenApiTypes.DATE,
            description="Productos creados antes de esta fecha.",
        ),
        OpenApiParameter(
            name="ordering",
            type=OpenApiTypes.STR,
            description=(
                "Ordenamiento. Ejemplos: created_at, -created_at, "
                "price, -price, stock, -stock."
            ),
        ),
    ],
    responses={
        200: ProductSerializer(many=True),
        201: ProductSerializer,
        400: OpenApiResponse(
            description="Datos inválidos."
        ),
        401: OpenApiResponse(
            description="Usuario no autenticado."
        ),
        403: OpenApiResponse(
            description="Usuario sin permisos."
        ),
    },
)
class ProductListCreateView(generics.ListCreateAPIView):

    serializer_class = ProductSerializer

    permission_classes = [
        ProductPermission
    ]

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]

    filterset_class = ProductFilter

    search_fields = [
        "name",
        "sku",
        "description",
        "category__name",
    ]

    ordering_fields = [
        "name",
        "price",
        "stock",
        "created_at",
    ]

    ordering = [
        "-created_at"
    ]

    def get_queryset(self):
        return ProductSelector.get_all()

    def perform_create(self, serializer):
        serializer.save()


#clase para listar productos activos

@extend_schema(
    tags=["Products"],
    summary="Obtener producto",
    description="""
    Obtiene la información de un producto específico.

    Permisos:
    - ADMIN: permitido.
    - SUPERVISOR: permitido.
    - EMPLOYEE: permitido.

    Autenticación:
    - Requiere Bearer JWT.
    """,
    responses={
        200: ProductSerializer,
        401: OpenApiResponse(
            description="Usuario no autenticado."
        ),
        404: OpenApiResponse(
            description="Producto no encontrado."
        ),
    },
)

#esta clase es para obtener, actualizar y eliminar un producto
class ProductDetailView(
    generics.RetrieveUpdateDestroyAPIView
):

    serializer_class = ProductSerializer
    permission_classes = [ProductPermission]


    def get_queryset(self):

        return ProductSelector.active_products()


    def perform_destroy(self, instance):

        ProductService.delete_product(
            instance,
            self.request.user,
        )


#clase para listar productos con stock bajo 
@extend_schema(
    tags=["Products"],
    summary="List low-stock products",
    description=(
        "Returns active products whose stock is at or below "
        "their configured minimum stock level."
    ),
    responses={
        200: ProductSerializer(many=True),
        401: OpenApiResponse(
            description="Authentication required."
        ),
        403: OpenApiResponse(
            description="User does not have permission."
        ),
    },
)
class ProductLowStockView(
    generics.ListAPIView
):

    serializer_class = ProductSerializer

    permission_classes = [
        ProductPermission,
    ]

    def get_queryset(self):

        return ProductSelector.low_stock()
    

#esta clase es para restaurar un producto eliminado

@extend_schema(
    tags=["Products"],
    summary="Restore deleted product",
    description=(
        "Restores a previously soft-deleted product. "
        "This operation is restricted to administrators."
    ),
    responses={
        200: ProductSerializer,
        401: OpenApiResponse(
            description="Authentication required."
        ),
        403: OpenApiResponse(
            description="Administrator permissions required."
        ),
        404: OpenApiResponse(
            description="Deleted product not found."
        ),
    },
)
class ProductRestoreView(generics.UpdateAPIView):

    serializer_class = ProductSerializer
    permission_classes = [IsAdmin]

    def get_queryset(self):
        return Product.objects.filter(
            is_deleted=True
        )

    def update(self, request, *args, **kwargs):

        product = self.get_object()

        product = ProductService.restore_product(
            product,
            request.user
        )

        serializer = self.get_serializer(product)

        return Response(
            serializer.data,
            status=200
        )
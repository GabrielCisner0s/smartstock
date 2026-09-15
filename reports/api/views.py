from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from drf_spectacular.utils import (
    extend_schema,
    OpenApiResponse,
)

from reports.api.serializers import DashboardSerializer
from reports.services import DashboardService


@extend_schema(
    tags=["Reports"],
    summary="Get system dashboard",
    description=(
        "Returns a general overview of the system, "
        "including relevant inventory and product metrics."
    ),
    responses={
        200: DashboardSerializer,
        401: OpenApiResponse(
            description="Authentication required."
        ),
    },
)
class DashboardView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def get(self, request):
        data = DashboardService.get_summary()
        serializer = DashboardSerializer(data)

        return Response(serializer.data)
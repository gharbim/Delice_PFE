from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .summary import get_forecast_summary


class ForecastSummaryViewSet(viewsets.ViewSet):
    permission_classes = (AllowAny,)

    def list(self, request, *args, **kwargs):
        try:
            return Response(get_forecast_summary(), status=status.HTTP_200_OK)
        except Exception as exc:
            return Response(
                {"success": False, "error": "Forecast summary failed."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

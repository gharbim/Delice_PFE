from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .serializers import PredictPriceRequestSerializer
from .predict import predict_price


class PricePredictionViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    permission_classes = (AllowAny,)
    serializer_class = PredictPriceRequestSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            predicted_premium = predict_price(serializer.validated_data)
            return Response(
                {"success": True, "predicted_premium": round(predicted_premium, 2)},
                status=status.HTTP_200_OK,
            )
        except Exception as exc:
            return Response(
                {"success": False, "error": "Premium prediction failed."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

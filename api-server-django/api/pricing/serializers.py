from rest_framework import serializers

from .predict import ALL_CITIES, LIB_USAGE_CHOICES


class PredictPriceRequestSerializer(serializers.Serializer):
    driver_age = serializers.FloatField(min_value=16, max_value=100)
    vehicle_age = serializers.FloatField(min_value=0, max_value=50)
    contract_tenure = serializers.FloatField(min_value=0, max_value=50)
    puissance = serializers.FloatField(min_value=1, max_value=40)
    bonus_malus = serializers.FloatField(min_value=0, max_value=200)
    ville = serializers.ChoiceField(choices=ALL_CITIES)
    lib_usage = serializers.ChoiceField(choices=LIB_USAGE_CHOICES)

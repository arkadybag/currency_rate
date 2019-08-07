from rest_framework import serializers

from main.models import Currency


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ['id', 'name']


class RateSerializer(serializers.Serializer):
    rate = serializers.FloatField()
    avg_volume = serializers.FloatField()

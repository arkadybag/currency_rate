from rest_framework import generics, status
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from main.models import Currency, Rate
from main.serializers import CurrencySerializer, RateSerializer
from main.util import ResultsSetPagination


class CurrencyView(generics.ListAPIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Currency.objects.order_by('id')
    serializer_class = CurrencySerializer
    pagination_class = ResultsSetPagination


class RateView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = RateSerializer

    def get(self, request, currency):
        rate = Rate.latest(currency)
        if not rate:
            return Response(status=status.HTTP_404_NOT_FOUND)

        avg_volume = Rate.average(currency, 10)

        resp = self.serializer_class({
            'rate': rate.rate,
            'avg_volume': avg_volume['volume__avg']
        })

        return Response(resp.data)

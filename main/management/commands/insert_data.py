import datetime
from collections import namedtuple

import requests
from django.core.management import BaseCommand
from pytz import UTC

from main.models import Currency, Rate

_Rate = namedtuple('_Rate', 'MTS OPEN CLOSE HIGH LOW VOLUME')


class Command(BaseCommand):
    CURRENCIES = 'https://api.bitfinex.com/v1/symbols'
    RATE = 'https://api-pub.bitfinex.com/v2/candles/trade:1D:t{rate}/hist'

    def _request(self, url):
        return requests.get(url).json()

    def _insert_currencies(self):
        currencies = self._request(self.CURRENCIES)[:10]

        for c in currencies:
            Currency.objects.get_or_create(name=c.upper())

    def _insert_rates(self):
        currencies = Currency.objects.all()

        for c in currencies:
            rates = self._request(self.RATE.format(rate=c.name))
            for r in rates:
                _rate = _Rate(*r)

                # division need because BITFINEX API return MTS lime millisecond time stamp
                # but python datetime.datetime.fromtimestamp required seconds
                mts = (
                    datetime.datetime
                        .fromtimestamp(_rate.MTS / 1000)
                        .astimezone(tz=UTC)
                )

                Rate.objects.get_or_create(
                    date=mts,
                    rate=_rate.CLOSE,
                    volume=_rate.VOLUME,
                    currency_id=c.id,
                )

    def handle(self, *args, **options):
        self._insert_currencies()
        self._insert_rates()

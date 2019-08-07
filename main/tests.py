import datetime

from django.contrib.auth.models import User
from django.test import TestCase
from pytz import UTC
from requests.auth import _basic_auth_str
from rest_framework import status
from rest_framework.test import APITestCase

from main.models import Rate, Currency


class CurrencyTestCase(TestCase):
    CURRENCY = 'BTCUSD'

    def setUp(self):
        Currency.objects.create(name=self.CURRENCY)

    def test_get_currency(self):
        currency = Currency.objects.get(name=self.CURRENCY)
        self.assertEqual(currency.name, self.CURRENCY)


class RateTestCase(TestCase):
    RATE = 10
    VOLUME = 100
    DATE = datetime.datetime.now().astimezone(tz=UTC)
    CURRENCY = 'BTCUSD'

    def setUp(self):
        currency = Currency.objects.create(name=self.CURRENCY)

        Rate.objects.create(
            currency=currency,
            date=self.DATE,
            rate=self.RATE,
            volume=self.VOLUME
        )

    def test_get_currency(self):
        currency = Currency.objects.get(name=self.CURRENCY)
        rate = Rate.objects.filter(currency=currency).first()

        self.assertEqual(rate.currency, currency)
        self.assertEqual(rate.rate, self.RATE)
        self.assertEqual(rate.volume, self.VOLUME)
        self.assertEqual(rate.date.isoformat(), self.DATE.isoformat())


class RateFunctionsTestCase(TestCase):
    RATE = 10
    VOLUME = 100
    DATE = datetime.datetime.now().astimezone(tz=UTC)
    CURRENCY = 'BTCUSD'
    LIMIT = 10

    def setUp(self):
        currency = Currency.objects.create(name=self.CURRENCY)

        for i in range(self.LIMIT):
            Rate.objects.create(
                currency=currency,
                date=self.DATE + datetime.timedelta(days=i),
                rate=self.RATE + i,
                volume=self.VOLUME + i
            )

    def test_get_latest(self):
        rate = Rate.objects \
            .filter(currency__name=self.CURRENCY) \
            .order_by('-date') \
            .first()

        latest = Rate.latest(self.CURRENCY)

        self.assertEqual(latest.id, rate.id)

    def test_get_average(self):
        avg_volume = Rate.average(self.CURRENCY, self.LIMIT)

        self.assertIn('volume__avg', avg_volume)
        self.assertEqual(avg_volume['volume__avg'], 104.5)


class ApiTestCase(APITestCase):
    RATE = 10
    VOLUME = 100
    DATE = datetime.datetime.now().astimezone(tz=UTC)
    CURRENCY = 'BTCUSD'
    LIMIT = 10

    def setUp(self):
        self.user = User.objects.create_user('test', password='test')
        currency = Currency.objects.create(name=self.CURRENCY)

        for i in range(self.LIMIT):
            Currency.objects.create(name=self.CURRENCY + str(i))

            Rate.objects.create(
                currency=currency,
                date=self.DATE + datetime.timedelta(days=i),
                rate=self.RATE + i,
                volume=self.VOLUME + i
            )

    def test_get_currency_without_auth_api_view(self):
        response = self.client.get('/currencies')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_rate_without_auth_api_view(self):
        response = self.client.get('/rate/{}/'.format(self.CURRENCY))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_currency_api_view(self):
        self.client.credentials(HTTP_AUTHORIZATION=_basic_auth_str('test', 'test'))

        response = self.client.get('/currencies')

        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data['count'], self.LIMIT + 1)
        self.assertEqual(data['results'][0]['name'], self.CURRENCY)

    def test_get_rate_api_view(self):
        self.client.credentials(HTTP_AUTHORIZATION=_basic_auth_str('test', 'test'))

        response = self.client.get('/rate/{}/'.format(self.CURRENCY))

        data = response.json()
        latest = Rate.latest(self.CURRENCY)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEquals(data['rate'], latest.rate, 19)
        self.assertEqual(data['avg_volume'], 104.5)

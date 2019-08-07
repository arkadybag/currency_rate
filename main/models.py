from django.db import models
from django.db.models import Avg


class Currency(models.Model):
    name = models.CharField(max_length=100)


class Rate(models.Model):
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    date = models.DateTimeField()
    rate = models.FloatField()
    volume = models.FloatField()

    @classmethod
    def latest(cls, currency):
        return cls.objects \
            .filter(currency__name=currency) \
            .order_by('-date') \
            .first()

    @classmethod
    def average(cls, currency, limit):
        rates = cls.objects \
                    .filter(currency__name=currency) \
                    .order_by('-date')[:limit]

        return rates.aggregate(Avg('volume'))

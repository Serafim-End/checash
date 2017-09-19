
from django.db import models

from bill.models import Bill


class Item(models.Model):

    name = models.CharField(max_length=64)
    description = models.CharField(max_length=128, blank=True, default='')

    price = models.IntegerField(default=-1)
    cashback = models.IntegerField(default=-1)

    bills = models.ForeignKey(
        Bill, models.CASCADE,
        related_name='items', null=True
    )

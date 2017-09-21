from django.db import models

from items.models import Item
from bill.models import Bill


class Promo(models.Model):

    # if you wanna use cashback without any items - just with simple condition
    items = models.ManyToManyField(Item, null=True)

    # to collect promos
    # it is possible to have a bill without any promos
    bills = models.ManyToManyField(
        Bill, models.CASCADE,
        related_name='promos', null=True
    )

    title = models.CharField(max_length=100)
    due_date = models.DateTimeField(blank=False)
    start_date = models.DateTimeField(auto_now=True)
    cashback_rub = models.IntegerField()
    lower_bound_rub = models.IntegerField()


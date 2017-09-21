from django.db import models

from items.models import Item


class Promo(models.Model):

    # if you wanna use cashback without any items - just with simple condition
    items = models.ForeignKey(Item, null=True, related_name='promos')

    title = models.CharField(max_length=100)
    due_date = models.DateTimeField(blank=False)
    start_date = models.DateTimeField(auto_now=True)
    cashback_rub = models.IntegerField()
    lower_bound_rub = models.IntegerField()


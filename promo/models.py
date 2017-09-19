from django.db import models

from items.models import Item


class Promo(models.Model):

    item = models.ForeignKey(Item)
    title = models.CharField(max_length=100)
    due_date = models.DateTimeField(blank=False)
    start_date = models.DateTimeField(auto_now=True)
    cashback_rub = models.IntegerField()
    lower_bound_rub = models.IntegerField()

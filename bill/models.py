from django.db import models
from django.contrib.postgres.fields import JSONField

from promo.service import PromoService


class Organization(models.Model):

    # retailPlaceAddress
    # address = models.CharField(max_length=50)

    # user - from the bill
    name = models.CharField(max_length=50)


class Bill(models.Model):

    # "buyerAddress": "",
    # "operationType": 1,
    # "receiptCode": 3,
    # "senderAddress": "",

    fiscalSign = models.IntegerField(primary_key=True)

    dateTime = models.DateTimeField(auto_now=True)
    nds18 = models.IntegerField(default=-1)
    taxation_type = models.IntegerField(default=-1)
    ecash_total_sum = models.IntegerField(default=-1)
    cashTotalSum = models.IntegerField(default=-1)
    total_sum = models.IntegerField(default=-1)
    operationType = models.IntegerField(default=-1)

    qr = JSONField(blank=True)

    # we should find items with discount from promo list
    cashback = models.IntegerField(default=-1)

    in_processing = models.BooleanField(default=True)

    def determine_cashback(self):

        active_promos = PromoService.get_active_promos()

        # the case just for one item in promo
        for item in self.items.all():
            for promo in active_promos.all():
                if (item in promo.items and
                        self.total_sum >= promo.lower_bound_rub):
                    self.promos.add(promo)
                    self.cashback += promo.cashback_rub


# class BillItem(models.Model):
#     bills = models.ForeignKey(Bill, models.CASCADE,
#                               related_name='bill_items')
#
#     price = models.IntegerField(default=-1)
#     cashback = models.IntegerField(default=-1)

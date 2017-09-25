from django.db import models
from django.contrib.postgres.fields import JSONField

from user.models import Person


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

    fiscalSign = models.BigIntegerField(primary_key=True)
    bills = models.ForeignKey(
        Person,
        on_delete=models.CASCADE, null=True, related_name='bills'
    )

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



# class BillItem(models.Model):
#     bills = models.ForeignKey(Bill, models.CASCADE,
#                               related_name='bill_items')
#
#     price = models.IntegerField(default=-1)
#     cashback = models.IntegerField(default=-1)

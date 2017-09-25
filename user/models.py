from django.contrib.auth.models import User
from django.db import models

from bill.models import Bill


class Person(User):

    bills = models.ForeignKey(Bill, on_delete=models.CASCADE, null=True)
    total_cashback = models.IntegerField(default=0)
    current_cashback = models.IntegerField(default=0)

    creation_time = models.DateTimeField(auto_now=True)

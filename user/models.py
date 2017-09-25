from django.contrib.auth.models import User
from django.db import models


class Person(User):

    total_cashback = models.IntegerField(default=0)
    current_cashback = models.IntegerField(default=0)
    creation_time = models.DateTimeField(auto_now=True)

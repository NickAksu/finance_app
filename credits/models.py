from django.db import models
from datetime import datetime

from accounts.models import Account


class Credit(models.Model):
    bank_account = models.ForeignKey(Account, on_delete=models.PROTECT)
    persent = models.DecimalField(max_digits=5, decimal_places=2)
    last_payed = models.DateField(default=datetime.now)
    total_sum = models.DecimalField(max_digits=15, decimal_places=2)
    sum_payed = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    is_differential = models.BooleanField(blank=False, default=True)
    period = models.IntegerField()
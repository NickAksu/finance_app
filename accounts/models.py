from django.db import models
import uuid


class Account(models.Model):
    account_id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4)
    
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    is_activated = models.BooleanField(default=False)
    saving_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    
class Operation(models.Model):
    sender = models.ForeignKey(Account, on_delete=models.DO_NOTHING, related_name="sender")
    reciever = models.ForeignKey(Account, on_delete=models.DO_NOTHING, related_name="reciever")
    sum_sent = models.IntegerField()
    date = models.DateField(auto_now=True)

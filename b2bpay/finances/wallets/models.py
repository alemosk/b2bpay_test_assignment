from decimal import Decimal

from django.db import models


class Wallet(models.Model):
    label = models.CharField(max_length=32)
    balance = models.DecimalField(max_digits=65, decimal_places=18, default=Decimal('0'))

    class Meta:
        db_table = 'finances_wallets'
        ordering = ('-id', )

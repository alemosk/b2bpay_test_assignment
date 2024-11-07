from decimal import Decimal

from django.db import models
from django.db.models import CheckConstraint, Q


class Wallet(models.Model):
    label = models.CharField(
        max_length=32,
        # we use index because we allow users to sort and filter data by this value.
        db_index=True,
    )
    balance = models.DecimalField(
        max_digits=65,
        decimal_places=18,
        default=Decimal('0'),
        # we use index because we allow users to sort and filter data by this value.
        db_index=True,
    )

    class Meta:
        db_table = 'finances_wallets'
        ordering = ('id', )
        constraints = [
            # DB: ADD CONSTRAINT wallet_balance_cant_be_negative CHECK (balance >= 0);
            CheckConstraint(condition=Q(balance__gte=0), name='wallet_balance_cant_be_negative')
        ]

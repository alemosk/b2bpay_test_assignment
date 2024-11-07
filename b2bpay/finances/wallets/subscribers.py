from decimal import Decimal

from django.db.models.signals import pre_save
from django.dispatch import receiver

from b2bpay.finances.wallets.exceptions import InsufficientFundsException
from b2bpay.finances.wallets.models import Wallet


@receiver(pre_save, sender=Wallet)
def negative_balance_protection(sender, instance, **kwargs):
    # Just another level of protection from negative balances before db exception

    if instance.balance < Decimal('0.0'):
        raise InsufficientFundsException

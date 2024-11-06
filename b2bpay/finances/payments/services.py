from decimal import Decimal

from django.db import transaction as tx
from rest_framework.exceptions import ValidationError

from b2bpay.finances.transactions.models import Transaction
from b2bpay.finances.wallets.models import Wallet


def deposit_to_wallet(wallet: Wallet, txid: str, amount: Decimal) -> Transaction:
    with tx.atomic():
        wallet = Wallet.objects.select_for_update(nowait=True).get(pk=wallet.pk)

        transaction = Transaction.objects.create(wallet=wallet, txid=txid, amount=amount)
        wallet.balance += amount
        wallet.save(update_fields=['balance'])

    return transaction


def withdrawal_from_wallet(wallet: Wallet, txid: str, amount: Decimal):
    with tx.atomic():
        wallet = Wallet.objects.select_for_update(nowait=True).get(pk=wallet.pk)

        if wallet.balance < amount:
            raise ValidationError(f'Wallet balance {wallet.balance} is less than withdrawal amount {amount}')

        transaction = Transaction.objects.create(wallet=wallet, txid=txid, amount=amount)
        wallet.balance -= amount
        wallet.save(update_fields=['balance'])

    return transaction

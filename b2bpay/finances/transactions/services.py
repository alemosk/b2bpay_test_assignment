from decimal import Decimal

from django.db import transaction as tx
from rest_framework.exceptions import ValidationError

from b2bpay.finances.transactions.models import Transaction
from b2bpay.finances.wallets.exceptions import InsufficientFundsException
from b2bpay.finances.wallets.models import Wallet
from b2bpay.finances.wallets.services import adjust_balance


def create_transaction(wallet: Wallet, txid: str, amount: Decimal) -> Transaction:
    with tx.atomic():
        wallet = Wallet.objects.select_for_update(nowait=True).get(pk=wallet.pk)

        transaction = Transaction.objects.create(wallet=wallet, txid=txid, amount=amount)

        try:
            adjust_balance(wallet, transaction.amount)
        except InsufficientFundsException as e:
            raise ValidationError(str(e))

    return transaction

from decimal import Decimal

from b2bpay.finances.wallets.exceptions import InsufficientFundsException
from b2bpay.finances.wallets.models import Wallet


def adjust_balance(wallet: Wallet, amount: Decimal, save: bool = True) -> Wallet:
    new_balance = wallet.balance + amount

    if new_balance < Decimal('0.0'):
        raise InsufficientFundsException

    wallet.balance = new_balance

    if save:
        wallet.save(update_fields=['balance'])

    return wallet

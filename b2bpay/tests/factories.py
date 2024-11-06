from decimal import Decimal

import factory
from factory import post_generation

from b2bpay.finances.transactions.models import Transaction
from b2bpay.finances.wallets.models import Wallet


class WalletFactory(factory.django.DjangoModelFactory):
    label = factory.Sequence(lambda n: f'wallet_id_{n + 1}')
    balance = Decimal('0')

    class Meta:
        model = Wallet


class TransactionFactory(factory.django.DjangoModelFactory):
    txid = factory.Sequence(lambda n: f'transaction_id_{n + 1}')
    amount = Decimal('100')

    class Meta:
        model = Transaction
        skip_postgeneration_save = True

    @factory.lazy_attribute
    def wallet(self):
        return WalletFactory()

    @post_generation
    def post(self, create, extracted, **kwargs):
        if create:
            self.wallet.balance += self.amount
            self.wallet.save()

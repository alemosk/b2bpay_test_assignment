from decimal import Decimal

from django.test import TestCase

from b2bpay.tests.factories import TransactionFactory, WalletFactory


class TransactionsTestCase(TestCase):

    def test_transaction_factory(self):
        transaction = TransactionFactory(amount=Decimal('100'))
        assert transaction.amount == Decimal('100')
        assert transaction.wallet.balance == Decimal('100')

        transaction = TransactionFactory(amount=Decimal('100'), wallet=WalletFactory())
        assert transaction.wallet.balance == Decimal('100')

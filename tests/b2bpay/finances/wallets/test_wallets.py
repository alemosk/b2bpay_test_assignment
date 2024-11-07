import re
from decimal import Decimal
from unittest.mock import patch

from django.db import IntegrityError
from django.test import TestCase

from b2bpay.finances.wallets.exceptions import InsufficientFundsException
from b2bpay.tests.factories import WalletFactory


class WalletsTestCase(TestCase):

    def test_wallet_factory(self):
        wallet_1 = WalletFactory()
        assert re.match(r'wallet_id_\d+', wallet_1.label)
        assert wallet_1.balance == Decimal('0')

        wallet_2 = WalletFactory(balance=Decimal('100'))
        assert wallet_1.label != wallet_2.label
        assert wallet_2.balance == Decimal('100')

    def test_negative_balance_protection_signal(self):
        wallet = WalletFactory(balance=Decimal('0'))
        wallet.balance = -1

        with self.assertRaises(InsufficientFundsException):
            wallet.save()

    def test_negative_balance_protection_factory(self):
        with self.assertRaises(InsufficientFundsException):
            WalletFactory(balance=Decimal('-0.000000000000000001'))

    @patch('django.db.models.base.pre_save')
    def test_negative_balance_protection_db(self, _):
        with self.assertRaises(IntegrityError):
            WalletFactory(balance=Decimal('-0.000000000000000001'))

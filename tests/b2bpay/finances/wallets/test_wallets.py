import re
from decimal import Decimal

from django.test import TestCase

from b2bpay.tests.factories import WalletFactory


class WalletsTestCase(TestCase):

    def test_wallet_factory(self):
        wallet_1 = WalletFactory()
        assert re.match(r'wallet_id_\d+', wallet_1.label)
        assert wallet_1.balance == Decimal('0')

        wallet_2 = WalletFactory(balance=Decimal('100'))
        assert wallet_1.label != wallet_2.label
        assert wallet_2.balance == Decimal('100')

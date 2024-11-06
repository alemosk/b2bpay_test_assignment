import uuid
from decimal import Decimal

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from b2bpay.tests.factories import WalletFactory


class PaymentsAPITestCase(APITestCase):
    def test_deposit_to_wallet(self):
        url = reverse('finances:payments:deposit')
        wallet = WalletFactory()

        txid = str(uuid.uuid4())
        data = {
            'data': {
                'type': 'Deposit',
                'attributes': {
                    'wallet': wallet.pk,
                    'txid': txid,
                    'amount': '100.00',
                }
            }
        }

        response = self.client.post(
            url,
            data=data,
        )

        wallet.refresh_from_db()

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['txid'] == txid
        assert response.data['amount'] == '100.000000000000000000'
        assert response.data['wallet']['id'] == str(wallet.pk)
        assert wallet.balance == Decimal('100.00')

    def test_withdrawal_from_wallet(self):
        url = reverse('finances:payments:withdrawal')

        wallet = WalletFactory(balance=Decimal('100'))

        txid = str(uuid.uuid4())
        data = {
            'data': {
                'type': 'Withdrawal',
                'attributes': {
                    'wallet': wallet.pk,
                    'txid': txid,
                    'amount': '100.00',
                }
            }
        }

        response = self.client.post(
            url,
            data=data,
        )

        wallet.refresh_from_db()

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['txid'] == txid
        assert response.data['amount'] == '100.000000000000000000'
        assert response.data['wallet']['id'] == str(wallet.pk)
        assert wallet.balance == Decimal('0.00')

        response = self.client.post(
            url,
            data=data,
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

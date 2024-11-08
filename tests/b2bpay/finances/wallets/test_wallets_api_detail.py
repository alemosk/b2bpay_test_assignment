from decimal import Decimal

from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from b2bpay.finances.wallets.models import Wallet
from b2bpay.tests.factories import WalletFactory, TransactionFactory


class WalletsAPITestCase(APITestCase):
    def test_get_wallet(self):
        wallet = WalletFactory()

        url = reverse('finances:wallets:detail', kwargs={
            'pk': wallet.pk
        })

        response = self.client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == wallet.pk

    def test_update_wallet_put(self):
        wallet = WalletFactory(label='Old label')

        url = reverse('finances:wallets:detail', kwargs={
            'pk': wallet.pk
        })

        new_label = 'put label'

        data = {
            'data': {
                'type': 'Wallet',
                'id': wallet.pk,
                'attributes': {
                    'label': new_label,
                }
            }
        }
        response = self.client.put(url, data=data)
        wallet.refresh_from_db()
        assert response.status_code == status.HTTP_200_OK
        assert wallet.label == new_label

    def test_update_wallet_patch(self):
        wallet = WalletFactory(label='Old label')

        url = reverse('finances:wallets:detail', kwargs={
            'pk': wallet.pk
        })

        new_label = 'patch label'

        data = {
            'data': {
                'type': 'Wallet',
                'id': wallet.pk,
                'attributes': {
                    'label': new_label,
                }
            }
        }
        response = self.client.patch(url, data=data)
        wallet.refresh_from_db()
        assert response.status_code == status.HTTP_200_OK
        assert wallet.label == new_label

    def test_update_wallet_balance(self):
        wallet = WalletFactory(label='Wallet', balance=Decimal('11.0'))

        url = reverse('finances:wallets:detail', kwargs={
            'pk': wallet.pk
        })

        data = {
            'data': {
                'type': 'Wallet',
                'id': wallet.pk,
                'attributes': {
                    'label': 'Wallet with balance',
                    'balance': Decimal('100.00')
                }
            }
        }
        response = self.client.put(url, data=data)
        wallet.refresh_from_db()
        assert response.status_code == status.HTTP_200_OK
        # Balance should not be updated
        assert wallet.balance == Decimal('11.0')

    def test_delete_empty_wallet(self):
        wallet = WalletFactory(label='Wallet', balance=Decimal('0.0'))

        url = reverse('finances:wallets:detail', kwargs={
            'pk': wallet.pk
        })

        response = self.client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT

        with self.assertRaises(wallet.DoesNotExist):
            wallet.refresh_from_db()

    def test_delete_wallet_with_transactions(self):
        transaction = TransactionFactory()
        wallet = transaction.wallet

        url = reverse('finances:wallets:detail', kwargs={
            'pk': wallet.pk
        })

        response = self.client.delete(url)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data[0]['detail'] == 'This wallet can not be removed'

        wallet = Wallet.objects.filter(pk=wallet.pk).first()
        assert wallet is not None

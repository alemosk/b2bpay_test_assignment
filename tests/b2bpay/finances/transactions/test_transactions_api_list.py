import uuid
from decimal import Decimal

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from b2bpay.tests.factories import TransactionFactory, WalletFactory


class TransactionsAPITestCase(APITestCase):
    def test_get_transactions_list(self):
        transaction = TransactionFactory()

        url = reverse('finances:transactions:list')

        response = self.client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['results'][0]['id'] == transaction.pk

    def test_deposit_transaction(self):
        url = reverse('finances:transactions:list')
        wallet = WalletFactory()

        txid = str(uuid.uuid4())
        data = {
            'data': {
                'type': 'Transaction',
                'attributes': {
                    'wallet': wallet.pk,
                    'txid': txid,
                    'amount': '100.00',
                }
            }
        }

        response = self.client.post(url, data=data)

        wallet.refresh_from_db()

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['txid'] == txid
        assert response.data['amount'] == '100.000000000000000000'
        assert response.data['wallet'] == wallet.pk
        assert wallet.balance == Decimal('100.00')

        # request with same txid
        response = self.client.post(url, data=data)

        wallet.refresh_from_db()

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_withdrawal_transaction(self):
        url = reverse('finances:transactions:list')

        wallet = WalletFactory(balance=Decimal('100'))

        txid = str(uuid.uuid4())
        data = {
            'data': {
                'type': 'Transaction',
                'attributes': {
                    'wallet': wallet.pk,
                    'txid': txid,
                    'amount': '-100.00',
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
        assert response.data['amount'] == '-100.000000000000000000'
        assert response.data['wallet'] == wallet.pk
        assert wallet.balance == Decimal('0.00')

        # Test wallet balance is zero
        data['data']['attributes']['txid'] = str(uuid.uuid4())
        response = self.client.post(
            url,
            data=data,
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data[0]['detail'] == 'Insufficient funds for this operation'

    def test_pagination(self):
        TransactionFactory()
        TransactionFactory()
        TransactionFactory()

        url = reverse('finances:transactions:list')

        response = self.client.get(url, query_params={'page[size]': 10})

        assert response.status_code == status.HTTP_200_OK
        assert response.data['meta']['pagination']['count'] == 3
        assert response.data['meta']['pagination']['page'] == 1
        assert response.data['meta']['pagination']['pages'] == 1

        response = self.client.get(url, query_params={
            'page[size]': 1,
            'page[number]': 3,
        })
        assert response.status_code == status.HTTP_200_OK
        assert response.data['meta']['pagination']['count'] == 3
        assert response.data['meta']['pagination']['page'] == 3
        assert response.data['meta']['pagination']['pages'] == 3

        response = self.client.get(url, query_params={
            'page[size]': 1,
            'page[number]': 2,
        })
        assert response.status_code == status.HTTP_200_OK
        assert response.data['meta']['pagination']['count'] == 3
        assert response.data['meta']['pagination']['page'] == 2
        assert response.data['meta']['pagination']['pages'] == 3

    def test_sorting(self):
        wallet_1 = WalletFactory(id=1)
        wallet_2 = WalletFactory(id=2)

        TransactionFactory(id=3, amount=Decimal('100'), txid='ab', wallet=wallet_1)
        TransactionFactory(id=1, amount=Decimal('120'), txid='bd', wallet=wallet_2)
        TransactionFactory(id=2, amount=Decimal('-50'), txid='bc', wallet=wallet_1)

        url = reverse('finances:transactions:list')

        # default sort by id asc
        response = self.client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['results'][0]['id'] == 1
        assert response.data['results'][1]['id'] == 2
        assert response.data['results'][2]['id'] == 3

        # sort by id desc
        response = self.client.get(url, query_params={
            'sort': '-id'
        })

        assert response.status_code == status.HTTP_200_OK
        assert response.data['results'][0]['id'] == 3
        assert response.data['results'][1]['id'] == 2
        assert response.data['results'][2]['id'] == 1

        # sort by amount asc
        response = self.client.get(url, query_params={
            'sort': 'amount'
        })

        assert response.status_code == status.HTTP_200_OK
        assert response.data['results'][0]['amount'] == '-50.000000000000000000'
        assert response.data['results'][1]['amount'] == '100.000000000000000000'
        assert response.data['results'][2]['amount'] == '120.000000000000000000'

        # sort by amount desc
        response = self.client.get(url, query_params={
            'sort': '-amount'
        })

        assert response.status_code == status.HTTP_200_OK
        assert response.data['results'][0]['amount'] == '120.000000000000000000'
        assert response.data['results'][1]['amount'] == '100.000000000000000000'
        assert response.data['results'][2]['amount'] == '-50.000000000000000000'

        # sort by txid  asc

        response = self.client.get(url, query_params={
            'sort': 'txid'
        })

        assert response.status_code == status.HTTP_200_OK
        assert response.data['results'][0]['txid'] == 'ab'
        assert response.data['results'][1]['txid'] == 'bc'
        assert response.data['results'][2]['txid'] == 'bd'

        # sort by txid  desc
        response = self.client.get(url, query_params={
            'sort': '-txid'
        })

        assert response.status_code == status.HTTP_200_OK
        assert response.data['results'][0]['txid'] == 'bd'
        assert response.data['results'][1]['txid'] == 'bc'
        assert response.data['results'][2]['txid'] == 'ab'

        # sort by wallet  asc
        response = self.client.get(url, query_params={
            'sort': 'wallet'
        })

        assert response.status_code == status.HTTP_200_OK
        assert response.data['results'][0]['wallet'] == 1
        assert response.data['results'][1]['wallet'] == 1
        assert response.data['results'][2]['wallet'] == 2

        # sort by wallet  desc
        response = self.client.get(url, query_params={
            'sort': '-wallet'
        })

        assert response.status_code == status.HTTP_200_OK
        assert response.data['results'][0]['wallet'] == 2
        assert response.data['results'][1]['wallet'] == 1
        assert response.data['results'][2]['wallet'] == 1

        # sort by multiple fields
        response = self.client.get(url, query_params={
            'sort': 'wallet,-amount'
        })

        assert response.status_code == status.HTTP_200_OK
        assert response.data['results'][0]['wallet'] == 1
        assert response.data['results'][0]['amount'] == '100.000000000000000000'
        assert response.data['results'][1]['wallet'] == 1
        assert response.data['results'][1]['amount'] == '-50.000000000000000000'
        assert response.data['results'][2]['wallet'] == 2
        assert response.data['results'][2]['amount'] == '120.000000000000000000'

    def test_filters(self):
        wallet_1 = WalletFactory(id=1)
        wallet_2 = WalletFactory(id=2)

        TransactionFactory(id=3, amount=Decimal('100'), txid='abc', wallet=wallet_1)
        TransactionFactory(id=1, amount=Decimal('120'), txid='def', wallet=wallet_2)
        TransactionFactory(id=2, amount=Decimal('-50'), txid='ghi', wallet=wallet_1)

        url = reverse('finances:transactions:list')

        # get transactions with id > 1
        response = self.client.get(url, query_params={
            'filter[id.gt]': 1,
        })

        assert response.status_code == status.HTTP_200_OK
        assert response.data['meta']['pagination']['count'] == 2
        assert response.data['results'][0]['id'] == 2
        assert response.data['results'][1]['id'] == 3

        # get transactions with balance < 120
        response = self.client.get(url, query_params={
            'filter[amount.lt]': 120,
        })

        assert response.status_code == status.HTTP_200_OK
        assert response.data['meta']['pagination']['count'] == 2
        assert response.data['results'][0]['id'] == 2
        assert response.data['results'][1]['id'] == 3

        # get transactions what txid start with d character
        response = self.client.get(url, query_params={
            'filter[txid.startswith]': 'd',
        })

        assert response.status_code == status.HTTP_200_OK
        assert response.data['meta']['pagination']['count'] == 1
        assert response.data['results'][0]['id'] == 1

        # get transactions using multiple filters
        response = self.client.get(url, query_params={
            'filter[amount]': 120,
            'filter[id]': 2,
        })

        assert response.status_code == status.HTTP_200_OK
        assert response.data['meta']['pagination']['count'] == 0

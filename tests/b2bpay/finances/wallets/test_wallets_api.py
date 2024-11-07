from decimal import Decimal

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from b2bpay.tests.factories import WalletFactory


class WalletsAPITestCase(APITestCase):
    def test_get_wallets_list(self):
        wallet = WalletFactory()

        url = reverse('finances:wallets:list')

        response = self.client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['results'][0]['id'] == wallet.pk

    def test_create_wallet(self):
        wallet = WalletFactory()

        url = reverse('finances:wallets:list')

        response = self.client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['results'][0]['id'] == wallet.pk

    def test_pagination(self):
        WalletFactory()
        WalletFactory()
        WalletFactory()

        url = reverse('finances:wallets:list')

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
        WalletFactory(id=3, balance=Decimal('100'), label='ab')
        WalletFactory(id=1, balance=Decimal('120'), label='bd')
        WalletFactory(id=2, balance=Decimal('100'), label='bc')

        url = reverse('finances:wallets:list')

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

        # sort by balance asc
        response = self.client.get(url, query_params={
            'sort': 'balance'
        })

        assert response.status_code == status.HTTP_200_OK
        assert response.data['results'][0]['balance'] == '100.000000000000000000'
        assert response.data['results'][1]['balance'] == '100.000000000000000000'
        assert response.data['results'][2]['balance'] == '120.000000000000000000'

        # sort by balance desc
        response = self.client.get(url, query_params={
            'sort': '-balance'
        })

        assert response.status_code == status.HTTP_200_OK
        assert response.data['results'][0]['balance'] == '120.000000000000000000'
        assert response.data['results'][1]['balance'] == '100.000000000000000000'
        assert response.data['results'][2]['balance'] == '100.000000000000000000'

        # sort by label  asc

        response = self.client.get(url, query_params={
            'sort': 'label'
        })

        assert response.status_code == status.HTTP_200_OK
        assert response.data['results'][0]['label'] == 'ab'
        assert response.data['results'][1]['label'] == 'bc'
        assert response.data['results'][2]['label'] == 'bd'

        # sort by txid  desc
        response = self.client.get(url, query_params={
            'sort': '-label'
        })

        assert response.status_code == status.HTTP_200_OK
        assert response.data['results'][0]['label'] == 'bd'
        assert response.data['results'][1]['label'] == 'bc'
        assert response.data['results'][2]['label'] == 'ab'

        # sort by multiple fields
        response = self.client.get(url, query_params={
            'sort': '-balance,label'
        })

        assert response.status_code == status.HTTP_200_OK
        assert response.data['results'][0]['label'] == 'bd'
        assert response.data['results'][0]['balance'] == '120.000000000000000000'
        assert response.data['results'][1]['label'] == 'ab'
        assert response.data['results'][1]['balance'] == '100.000000000000000000'
        assert response.data['results'][2]['label'] == 'bc'
        assert response.data['results'][2]['balance'] == '100.000000000000000000'

    def test_filters(self):
        WalletFactory(id=3, balance=Decimal('100'), label='abc')
        WalletFactory(id=1, balance=Decimal('120'), label='def')
        WalletFactory(id=2, balance=Decimal('100'), label='ghi')

        url = reverse('finances:wallets:list')

        # get wallets with id > 1
        response = self.client.get(url, query_params={
            'filter[id.gt]': 1,
        })

        assert response.status_code == status.HTTP_200_OK
        assert response.data['meta']['pagination']['count'] == 2
        assert response.data['results'][0]['id'] == 2
        assert response.data['results'][1]['id'] == 3

        # get wallets with balance < 120
        response = self.client.get(url, query_params={
            'filter[balance.lt]': 120,
        })

        assert response.status_code == status.HTTP_200_OK
        assert response.data['meta']['pagination']['count'] == 2
        assert response.data['results'][0]['id'] == 2
        assert response.data['results'][1]['id'] == 3

        # get wallets what label start with d character
        response = self.client.get(url, query_params={
            'filter[label.startswith]': 'd',
        })

        assert response.status_code == status.HTTP_200_OK
        assert response.data['meta']['pagination']['count'] == 1
        assert response.data['results'][0]['id'] == 1

        # get wallets using multiple filters
        response = self.client.get(url, query_params={
            'filter[balance]': 120,
            'filter[id]': 2,
        })

        assert response.status_code == status.HTTP_200_OK
        assert response.data['meta']['pagination']['count'] == 0

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

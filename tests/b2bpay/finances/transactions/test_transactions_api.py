from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from b2bpay.tests.factories import TransactionFactory


class TransactionsAPITestCase(APITestCase):
    def test_get_transactions_list(self):
        transaction = TransactionFactory()

        url = reverse('finances:transactions:list')

        response = self.client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['results'][0]['id'] == transaction.pk

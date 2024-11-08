from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from b2bpay.tests.factories import TransactionFactory


class TransactionsAPITestCase(APITestCase):
    def test_get_transaction(self):
        transaction = TransactionFactory()

        url = reverse('finances:transactions:detail', kwargs={
            'pk': transaction.pk,
        })

        response = self.client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == transaction.pk

from rest_framework.generics import ListAPIView

from b2bpay.finances.transactions.models import Transaction
from b2bpay.finances.transactions.serializers import TransactionSerializer


class TransactionsListAPIView(ListAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

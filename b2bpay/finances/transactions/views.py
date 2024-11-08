from rest_framework.generics import ListCreateAPIView, RetrieveAPIView
from rest_framework_json_api import django_filters, filters

from b2bpay.finances.transactions.models import Transaction
from b2bpay.finances.transactions.serializers import TransactionSerializer


class TransactionsListCreateAPIView(ListCreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    filter_backends = (
        filters.QueryParameterValidationFilter,
        filters.OrderingFilter,
        django_filters.DjangoFilterBackend
    )

    filterset_fields = {
       'id': ('exact', 'lt', 'gt', 'gte', 'lte', 'in'),
       'amount': ('exact', 'lt', 'gt', 'gte', 'lte', 'in'),
       'wallet': ('exact', 'lt', 'gt', 'gte', 'lte', 'in'),
       'txid': ('exact', 'iexact', 'startswith'),
    }
    ordering_fields = ['id', 'amount', 'wallet', 'txid']


class TransactionsDetailAPIView(RetrieveAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

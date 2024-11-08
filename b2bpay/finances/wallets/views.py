from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework_json_api import django_filters, filters

from b2bpay.finances.wallets.models import Wallet
from b2bpay.finances.wallets.serializers import WalletSerializer


class WalletsListCreateAPIView(ListCreateAPIView):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer

    filter_backends = (
        filters.QueryParameterValidationFilter,
        filters.OrderingFilter,
        django_filters.DjangoFilterBackend
    )

    filterset_fields = {
       'id': ('exact', 'lt', 'gt', 'gte', 'lte', 'in'),
       'balance': ('exact', 'lt', 'gt', 'gte', 'lte', 'in'),
       'label': ('exact', 'iexact', 'startswith'),
    }


class WalletsDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer

    def perform_destroy(self, instance):
        # we should check that wallet doesn't contain any transactions
        if instance.transactions.exists():
            raise ValidationError('This wallet can not be removed')

        super().perform_destroy(instance)

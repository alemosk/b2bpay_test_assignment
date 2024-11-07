from rest_framework.generics import ListCreateAPIView

from b2bpay.finances.wallets.models import Wallet
from b2bpay.finances.wallets.serializers import WalletSerializer
from rest_framework_json_api import filters
from rest_framework_json_api import django_filters


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

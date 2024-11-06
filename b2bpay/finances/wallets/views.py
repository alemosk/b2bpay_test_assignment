from rest_framework.generics import ListCreateAPIView

from b2bpay.finances.wallets.models import Wallet
from b2bpay.finances.wallets.serializers import WalletSerializer


class WalletsListCreateAPIView(ListCreateAPIView):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer

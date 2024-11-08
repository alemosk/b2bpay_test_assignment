from rest_framework_json_api import serializers

from b2bpay.finances.wallets.models import Wallet


class WalletSerializer(serializers.ModelSerializer):
    balance = serializers.DecimalField(max_digits=64, decimal_places=18, read_only=True)

    class Meta:
        model = Wallet
        fields = '__all__'

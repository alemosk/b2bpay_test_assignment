from rest_framework_json_api import serializers

from b2bpay.finances.transactions.models import Transaction
from b2bpay.finances.wallets.models import Wallet


class TransactionSerializer(serializers.ModelSerializer):
    amount = serializers.DecimalField(max_digits=64, decimal_places=18)
    wallet = serializers.PrimaryKeyRelatedField(queryset=Wallet.objects.all())

    class Meta:
        model = Transaction
        fields = '__all__'

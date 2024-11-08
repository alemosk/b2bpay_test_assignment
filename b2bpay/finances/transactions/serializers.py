from rest_framework_json_api import serializers

from b2bpay.finances.transactions.models import Transaction
from b2bpay.finances.transactions.services import create_transaction
from b2bpay.finances.wallets.models import Wallet


class TransactionSerializer(serializers.ModelSerializer):
    amount = serializers.DecimalField(max_digits=64, decimal_places=18)
    wallet = serializers.PrimaryKeyRelatedField(queryset=Wallet.objects.all())

    class Meta:
        model = Transaction
        fields = '__all__'

    def save(self, **kwargs):
        # the save logic implemented in the different method due to balance calculation and balance check reason.
        transaction = create_transaction(
            self.validated_data['wallet'],
            self.validated_data['txid'],
            self.validated_data['amount'],
        )
        self.instance = transaction

        return self.instance

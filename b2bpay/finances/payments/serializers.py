from rest_framework_json_api import serializers

from b2bpay.finances.wallets.models import Wallet


class PaymentOperationRequestSerializer(serializers.Serializer):
    wallet = serializers.PrimaryKeyRelatedField(queryset=Wallet.objects.all())
    txid = serializers.CharField(max_length=64)
    amount = serializers.DecimalField(max_digits=65, decimal_places=18)


class PaymentOperationResponseSerializer(serializers.Serializer):
    status = serializers.CharField()


class DepositToWalletRequestSerializer(PaymentOperationRequestSerializer):
    pass


class WithdrawalFromWalletRequestSerializer(PaymentOperationRequestSerializer):
    pass

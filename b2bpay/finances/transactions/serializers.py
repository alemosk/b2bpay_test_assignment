from rest_framework_json_api import serializers

from b2bpay.finances.transactions.models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    amount = serializers.DecimalField(max_digits=64, decimal_places=18)

    class Meta:
        model = Transaction
        fields = '__all__'

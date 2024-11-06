from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from b2bpay.finances.payments.serializers import DepositToWalletRequestSerializer, WithdrawalFromWalletRequestSerializer
from b2bpay.finances.payments.services import deposit_to_wallet, withdrawal_from_wallet
from b2bpay.finances.transactions.serializers import TransactionSerializer


class DepositToWalletAPIView(APIView):
    resource_name = 'Deposit'

    def post(self, request, *args, **kwargs):
        serializer = DepositToWalletRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        transaction = deposit_to_wallet(
            wallet=serializer.validated_data['wallet'],
            txid=serializer.validated_data['txid'],
            amount=serializer.validated_data['amount']
        )

        return Response(
            data=TransactionSerializer().to_representation(instance=transaction),
            status=status.HTTP_201_CREATED
        )


class WithdrawalFromWalletAPIView(APIView):
    resource_name = 'Withdrawal'

    def post(self, request, *args, **kwargs):
        serializer = WithdrawalFromWalletRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        transaction = withdrawal_from_wallet(
            wallet=serializer.validated_data['wallet'],
            txid=serializer.validated_data['txid'],
            amount=serializer.validated_data['amount']
        )

        return Response(
            data=TransactionSerializer().to_representation(instance=transaction),
            status=status.HTTP_201_CREATED
        )


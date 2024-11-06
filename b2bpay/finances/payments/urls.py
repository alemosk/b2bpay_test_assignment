from django.urls import path

from b2bpay.finances.payments.views import DepositToWalletAPIView, WithdrawalFromWalletAPIView

app_name = "payments"

urlpatterns = [
    path('deposit/', DepositToWalletAPIView.as_view(), name='deposit'),
    path('withdrawal/', WithdrawalFromWalletAPIView.as_view(), name='withdrawal'),
]

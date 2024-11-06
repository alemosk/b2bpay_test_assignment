from django.urls import path

from b2bpay.finances.transactions.views import TransactionsListAPIView

app_name = "transactions"

urlpatterns = [
    path('', TransactionsListAPIView.as_view(), name='list'),
]

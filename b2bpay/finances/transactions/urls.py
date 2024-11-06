from django.urls import path

from b2bpay.finances.transactions.views import TransactionsAPIView

app_name = "transactions"

urlpatterns = [
    path('', TransactionsAPIView.as_view(), name='list'),
]

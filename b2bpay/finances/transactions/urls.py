from django.urls import path

from b2bpay.finances.transactions.views import TransactionsListCreateAPIView

app_name = "transactions"

urlpatterns = [
    path('', TransactionsListCreateAPIView.as_view(), name='list'),
]

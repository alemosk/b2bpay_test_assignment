from django.urls import path

from b2bpay.finances.transactions.views import TransactionsDetailAPIView, TransactionsListCreateAPIView

app_name = "transactions"

urlpatterns = [
    path('', TransactionsListCreateAPIView.as_view(), name='list'),
    path('<int:pk>/', TransactionsDetailAPIView.as_view(), name='detail'),
]

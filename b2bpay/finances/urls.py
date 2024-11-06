from django.urls import include, path

app_name = "finances"

urlpatterns = [
    path('wallets/', include('b2bpay.finances.wallets.urls'), name='wallets'),
    path('transactions/', include('b2bpay.finances.transactions.urls'), name='transactions'),
    path('payments/', include('b2bpay.finances.payments.urls'), name='payments'),
]

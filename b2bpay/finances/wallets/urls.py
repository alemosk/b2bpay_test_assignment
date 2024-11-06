from django.urls import path

from b2bpay.finances.wallets.views import WalletsListCreateAPIView

app_name = "wallets"

urlpatterns = [
    path('', WalletsListCreateAPIView.as_view(), name='list'),
]

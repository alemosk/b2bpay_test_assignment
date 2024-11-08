from django.urls import path

from b2bpay.finances.wallets.views import WalletsListCreateAPIView, WalletsDetailAPIView

app_name = "wallets"

urlpatterns = [
    path('', WalletsListCreateAPIView.as_view(), name='list'),
    path('wallets/<int:pk>/', WalletsDetailAPIView.as_view(), name='detail'),
]

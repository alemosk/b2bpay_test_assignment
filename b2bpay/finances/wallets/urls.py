from django.urls import path

from b2bpay.finances.wallets.views import WalletsDetailAPIView, WalletsListCreateAPIView

app_name = "wallets"

urlpatterns = [
    path('', WalletsListCreateAPIView.as_view(), name='list'),
    path('<int:pk>/', WalletsDetailAPIView.as_view(), name='detail'),
]

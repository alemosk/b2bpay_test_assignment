from django.urls import include, path

urlpatterns = [
    path('finances/', include('b2bpay.finances.urls'), name='finances'),
]

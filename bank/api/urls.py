from .views import AccountView, CustomerView, ReplenishmentView, TransactionView, TransferView
from django.urls import path, include


urlpatterns = [
    path('auth/', include('rest_framework.urls')),
    path('accounts/', AccountView.as_view({'get': 'list', 'post':'create'})),
    path('customers/', CustomerView.as_view({'get': 'list', 'post': 'create'})),
    path('customer/<int:pk>/', CustomerView.as_view({'get': 'retrieve'})),
    path('replenishment/', ReplenishmentView.as_view({'get': 'list', 'post': 'create'})),
    path('transactions/', TransactionView.as_view({'get': 'list', 'post': 'create'})),
    path('transfers/', TransferView.as_view({'get': 'list', 'post': 'create'})),
]

from .views import AccountView, CustomerView
from django.urls import path, include


urlpatterns = [
    path('auth/', include('rest_framework.urls')),
    path('accounts/', AccountView.as_view({'get': 'list', 'post':'create'})),
    path('customers/', CustomerView.as_view({'get': 'list', 'post': 'create'})),
    path('customer/<int:pk>/', CustomerView.as_view({'get': 'retrieve'}))
]

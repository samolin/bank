from .views import AccountView
from django.urls import path


urlpatterns = [
    path('accounts/', AccountView.as_view({'get': 'list', 'post':'create'})),
]

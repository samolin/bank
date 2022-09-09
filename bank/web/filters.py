from dataclasses import field
import django_filters
from api.models import Transaction, Transfer
from django_filters import DateFromToRangeFilter
from django_filters.widgets import DateRangeWidget


class TransactionFilter(django_filters.FilterSet):
    date = DateFromToRangeFilter(widget=DateRangeWidget(attrs={'class': 'datepicker', 'type': 'date'}))

    class Meta:
        model = Transaction
        fields = ['date', 'purchase']

class TransferFilter(django_filters.FilterSet):
    class Meta: 
        model = Transfer
        fields = ['from_account', 'to_account', 'amount']
      

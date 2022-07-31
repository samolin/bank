from django.contrib import admin
from .models import Customer, Account, Replenishment, Transaction, Transfer

admin.site.register(Customer)
admin.site.register(Account)
admin.site.register(Replenishment)
admin.site.register(Transaction)
admin.site.register(Transfer)

from django.contrib import admin
from .models import Account, Customer, Replenishment, Transaction, Transfer
from users.models import CustomUser

admin.site.register(Account)
admin.site.register(Customer)
admin.site.register(Replenishment)
admin.site.register(Transaction)
admin.site.register(Transfer)
admin.site.register(CustomUser)

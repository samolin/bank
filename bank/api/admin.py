from django.contrib import admin
from .models import Account, Customer, Replenishment, Transaction, Transfer
from users.models import CustomUser

admin.site.register(Account)
admin.site.register(Customer)

@admin.register(Replenishment)
class Replenishment(admin.ModelAdmin):
    list_display = ['id', 'date', 'amount', 'account']
    search_fields = ['date']

admin.site.register(Transaction)
admin.site.register(Transfer)
admin.site.register(CustomUser)

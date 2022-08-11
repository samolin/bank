from django.db import models, transaction
import uuid
from django.conf import settings
import os


class Customer(models.Model):

    def customer_image_file_path(instan, filename):
        ext = filename.split('.')[-1]
        filename = f'{uuid.uuid4()}.{ext}'
        return os.path.join('upload/customer/'+filename)

    name = models.CharField(max_length=40)
    surname = models.CharField(max_length=40)
    city = models.CharField(max_length=40)
    age = models.IntegerField()
    image = models.ImageField(null=True, upload_to=customer_image_file_path)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.surname} {self.name}'

class Account(models.Model):
    balance = models.DecimalField(default=0, max_digits=12, decimal_places=2)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.user.username}: account {self.id}'

class Replenishment(models.Model):
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    account = models.ForeignKey(Account, on_delete=models.CASCADE,
                                related_name='replenishment')
    
    @property
    def replenishment_date(self):
        date = self.date.strftime("%d.%m.%Y %H:%M:%S")
        return f"Amount: {str(self.amount)} - Date: {date}"

    def __str__(self):
        return f'Account {self.account.id} was topped up on {str(self.amount)}'
    
    @classmethod
    def top_up(cls, amount, account):
        if amount <= 0:
            raise(ValueError('Replenichment must be more than 0'))
        with transaction.atomic():
            account.balance += amount
            account.save()
            return account, amount

class Transaction(models.Model):
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    purchase = models.CharField(max_length=255)

    def __str__(self):
        return f'Account: {self.account.id} bought {self.purchase} for {self.amount}'

    @property
    def transaction_date(self):
        date = self.date.strftime("%d.%m.%Y %H:%M:%S")
        return date

    @classmethod
    def buy(cls, amount, account, purchase):
        if amount > account.balance:
            raise ValueError("You don't have enough money")
        account.balance -= amount
        account.save()
        return account, amount

class Transfer(models.Model):
    from_account = models.ForeignKey(Account, on_delete=models.CASCADE,
                                     related_name='from_account')
    to_account = models.ForeignKey(Account, on_delete=models.CASCADE,
                                     related_name='to_account')
    amount = models.DecimalField(max_digits=12, decimal_places=2)

    @classmethod
    def make_transfer(cls, from_account, to_account, amount):
        if amount > from_account.balance:
            raise ValueError("You don't have enough money")
        with transaction.atomic():
            from_account.balance -= amount
            to_account.balance += amount
            from_account.save()
            to_account.save()
            return from_account, to_account, amount
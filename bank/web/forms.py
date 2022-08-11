from users.models import CustomUser
from django import forms
from api.models import Replenishment, Transaction, Transfer


class UserRegistartionForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat Password', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['username', 'email']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError("Password doesn't match")
        return cd['password2']

class LoginUser(forms.ModelForm):
    username = forms.CharField(label='Username'),
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta: 
        model = CustomUser
        fields = ['username', 'password']
    
class ReplenishmentForm(forms.ModelForm):

    class Meta:
        model = Replenishment
        fields = ['account', 'amount']

class TransactionForm(forms.ModelForm):

    class Meta:
        model = Transaction
        fields = ['account', 'amount', 'purchase']
        
class TransferForm(forms.ModelForm):

    class Meta:
        model = Transfer
        fields = ['from_account', 'to_account', 'amount']
    
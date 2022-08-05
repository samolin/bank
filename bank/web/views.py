from django.shortcuts import render
from requests import request
from api.models import Customer, Account
from .forms import UserRegistartionForm
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.shortcuts import get_object_or_404


def index(request):
    if request.user.is_authenticated:
        data = Customer.objects.get(user=request.user)
        context = {
            'name': data.name,
            'surname': data.surname,
            'age': data.age,
            'city': data.city,
            'image': data.image
        }
        return render(request, 'web/web.html', context)
    return render(request, 'web/web.html', )    

def register(request):
    if request.method == 'POST':
        user_form = UserRegistartionForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return render(request, 'registration/register_done.html', {'new_user': new_user})
    else: 
        user_form = UserRegistartionForm()
        return render(request, 'registration/register.html', {'user_form': user_form})

    

class AccountView(generic.ListView):
    model = Account
    template_name = 'web/account.html'
    def get_queryset(self):
        return Account.objects.filter(user=self.request.user)

    #def get_queryset(self):
    #    self.account = get_object_or_404(Account)
    #    return Account.objects.filter(user=self.request.user)
#
    #data = Account.objects.filter(user=request.user)
#
    #print(data)
    #context = {
    #    data.balance
    #}
    #return render(request, 'web/account.html', context)


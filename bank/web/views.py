from django.shortcuts import render
from api.models import Customer, Account, Replenishment, Transaction, Transfer
from .forms import UserRegistartionForm, ReplenishmentForm, TransactionForm, TransferForm
from django.views.generic.edit import CreateView
from .filters import TransactionFilter, TransferFilter

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
    

class AccountView(CreateView):
    form_class = ReplenishmentForm
    template_name = 'web/account.html'
    success_url = '/account'

    def get_context_data(self, **kwargs):
        if not self.request.user.is_superuser:
            kwargs['object_list'] = Account.objects.filter(user=self.request.user)
            return super(AccountView, self).get_context_data(**kwargs)
        kwargs['object_list'] = Account.objects.all()
        return super(AccountView, self).get_context_data(**kwargs)
    
    def form_valid(self, form):
        response = super().form_valid(form)
        Replenishment.top_up(**form.cleaned_data)
        return response

class TransactionView(CreateView):
    form_class = TransactionForm
    template_name = 'web/transaction.html'
    success_url = '/transaction'

    def get_context_data(self, **kwargs):
        if self.request.user.is_superuser:
            kwargs['object_list'] = TransactionFilter(self.request.GET, queryset=Transaction.objects.all())
            return super(TransactionView, self).get_context_data(**kwargs)
        accounts = Account.objects.filter(user=self.request.user)
        kwargs['object_list'] = TransactionFilter(self.request.GET, queryset=Transaction.objects.filter(account__in=accounts))
        return super(TransactionView, self).get_context_data(**kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        Transaction.buy(**form.cleaned_data)
        return response

    def get_form_kwargs(self):
        kwargs = super(TransactionView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

class TransferView(CreateView):
    form_class = TransferForm
    template_name = 'web/transfer.html'
    success_url = '/transfer'

    def get_context_data(self, **kwargs):
        kwargs['object_list'] = TransferFilter(self.request.GET, queryset=Transfer.objects.all())
        return super(TransferView, self).get_context_data(**kwargs)





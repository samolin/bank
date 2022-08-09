from .serializers import AccountSerializer, CustomerSerializer, ReplenishmentSerializer, TransactionSerializer
from rest_framework import mixins, viewsets
from .models import Account, Customer, Replenishment, Transaction
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework import status


class AccountView(viewsets.GenericViewSet,
                  mixins.CreateModelMixin,
                  mixins.ListModelMixin):

    serializer_class = AccountSerializer
    queryset = Account.objects.all()
    permission_classes = [IsAuthenticated,]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
class CustomerView(viewsets.GenericViewSet,
                   mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   mixins.RetrieveModelMixin):
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()
    permission_classes = [IsAuthenticated,]

    def perform_create(self, serializer):
        if Customer.objects.filter(user=self.request.user.id).exists():
            raise ValidationError("You've already have your profile")
        serializer.save(user=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class ReplenishmentView(viewsets.GenericViewSet,
                        mixins.ListModelMixin,
                        mixins.CreateModelMixin):

    serializer_class = ReplenishmentSerializer
    queryset = Replenishment.objects.all()
    permission_classes = [IsAuthenticated,]

    def get_queryset(self):
        accounts = Account.objects.filter(user=self.request.user)
        return self.queryset.filter(account__in=accounts)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            Replenishment.top_up(**serializer.validated_data)
            serializer.save()
        except ValueError:
            content = {'error': 'You have to add more than 0'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class TransactionView(viewsets.GenericViewSet,
                      mixins.ListModelMixin,
                      mixins.CreateModelMixin):
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()
    permission_classes = [IsAuthenticated,]

    def get_queryset(self):
        accounts = Account.objects.filter(user=self.request.user)
        return self.queryset.filter(account__in=accounts)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            Transaction.buy(**serializer.validated_data)
            serializer.save()
        except:
            content = 'There is not enough money'
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    
        
    




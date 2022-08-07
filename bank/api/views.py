from .serializers import AccountSerializer, CustomerSerializer, ReplenishmentSerializer
from rest_framework import generics, mixins, viewsets
from .models import Account, Customer, Replenishment
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
        print(Account.objects.filter(user=self.request.user).get(pk=self.request.data['account']))
        try:
            account = Account.objects.filter(user=self.request.user).get(pk=self.request.data['account'])
        except Exception:
            return Response('No such account', status=status.HTTP_400_BAD_REQUEST)
        serializer.save(account=account)
        return Response(serializer.data, status=status.HTTP_201_CREATED, )


    
        
    




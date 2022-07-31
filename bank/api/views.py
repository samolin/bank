from .serializers import AccountSerializer, CustomerSerializer
from rest_framework import generics, mixins, viewsets
from .models import Account, Customer


class AccountView(viewsets.GenericViewSet,
                  mixins.CreateModelMixin,
                  mixins.ListModelMixin):
    serializer_class = AccountSerializer
    queryset = Account.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        





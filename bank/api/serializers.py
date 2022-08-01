from rest_framework import serializers
from .models import Account, Customer
from bank.settings import AUTH_USER_MODEL


class AccountSerializer(serializers.ModelSerializer):
    replenishment = serializers.SlugRelatedField(slug_field='replenishment_date',  many=True, read_only=True)

    class Meta:
        model = Account
        fields = ['id', 'balance', 'replenishment']
        read_only_fields = ['id', 'balance', 'replenishment']

class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = ['id', 'name', 'surname', 'age', 'city', 'image']
        read_only_fields = ['id',]

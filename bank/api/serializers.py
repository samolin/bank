from rest_framework import serializers
from .models import Account, Customer


class AccountSerializer(serializers.ModelSerializer):
    replenishment = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Account
        fields = ['id', 'balance', 'replenishment']
        read_only_fields = ['id', 'balance', 'replenishment']

class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = ['id', 'name' 'surname', 'age', 'city', 'user.id']
        read_only_fields = ['id',]

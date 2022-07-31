from rest_framework import serializers
from .models import Account, Customer


class CustomerSerializer(serializers.ModelSerializer):
    actions = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    
    class Meta:
        model = Account
        fields = ['id', 'balance', 'replenishment']
        read_only_fields = ['id',]

class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = ['id', 'name' 'surname', 'age', 'city', 'user.id']
        read_only_fields = ['id',]

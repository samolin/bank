from requests import request
from rest_framework import serializers
from .models import Account, Customer, Replenishment
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

class ReplenishmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Replenishment
        fields = ['id', 'amount', 'date', 'account']
        read_only_fields = ['id', 'date']

    def __init__(self, *args, **kwargs):
        super(ReplenishmentSerializer, self).__init__(*args, **kwargs)
        if 'request' in self.context:
            self.fields['account'].queryset = self.fields['account'].queryset.filter(user=self.context['view'].request.user)
        
    def create(self, validated_data):
        if validated_data['amount'] > 0:    
            validated_data['account'].balance += validated_data['amount']
            validated_data['account'].save()
        else:
            raise serializers.ValidationError('You have to put more than 0')
        return super(ReplenishmentSerializer, self).create(validated_data)


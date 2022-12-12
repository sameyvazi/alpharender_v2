from rest_framework import serializers
from .models import Transaction, UserBalance


class TransactionSerializer(serializers.ModelSerializer):
    transaction_type = serializers.IntegerField(required=True)
    amount = serializers.DecimalField(max_digits=10, decimal_places=3)

    class Meta:
        model = Transaction
        fields = ['id', 'user', 'amount', 'transaction_type']


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id']


class BalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBalance
        fields = '__all__'

from rest_framework import viewsets, permissions
from transaction.serializers import TransactionSerializer, ReportSerializer, BalanceSerializer
from transaction.models import Transaction, UserBalance
from rest_framework.response import Response
from django.db.models import Count, Sum, Q, FloatField
from django.db.models.functions import Coalesce

from django.contrib.auth.models import User
from rest_framework.decorators import action


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    http_method_names = ['get', 'post']
    serializer_class = TransactionSerializer


class ReportModelViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    http_method_names = ['get']
    serializer_class = ReportSerializer

    @action(detail=False)
    def report(self, request):
        # current_user = request.user.id
        current_user = 2

        positive_transactions = Sum(
            'transactions__amount',
            filter=Q(transactions__transaction_type=Transaction.CHARGE) & Q(transactions__user=current_user)
        )

        negative_transactions = Sum(
            'transactions__amount',
            filter=Q(transactions__transaction_type=Transaction.PURCHASE) & Q(transactions__user=current_user)
        )

        users = User.objects.filter(pk=current_user).annotate(
            tranaction_count=Count('transactions__id'),
            balance=Coalesce(positive_transactions, 0) - Coalesce(negative_transactions, 0)
        )

        return Response(users.first().balance)

        # recent_users = Transaction.objects.filter(user=1)
        # serializer = self.get_serializer(recent_users, many=True)
        # return Response(serializer.data)

    @action(detail=False)
    def balance(self, request):
        balance = Transaction.get_balance(request.user)
        return Response(balance)

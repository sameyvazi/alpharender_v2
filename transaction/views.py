from rest_framework import viewsets, permissions
from transaction.serializers import TransactionSerializer, ReportSerializer
from transaction.models import Transaction
from rest_framework.response import Response

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
        recent_users = Transaction.objects.filter(user=1)
        serializer = self.get_serializer(recent_users, many=True)
        return Response(serializer.data)



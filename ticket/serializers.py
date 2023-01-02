from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Ticket, Department


class DepartmentSerializers(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'title']


class TicketReadSerializer(serializers.ModelSerializer):
    department = DepartmentSerializers()

    extra = serializers.SerializerMethodField('count')

    def count(self, request):
        return request.user.username

    class Meta:
        model = Ticket
        fields = ['id', 'user', 'department', 'subject', 'message', 'file', 'extra']


class TicketSerializer(serializers.ModelSerializer):
    subject = serializers.CharField(required=True, max_length=256)
    message = serializers.CharField(required=True)

    class Meta:
        model = Ticket
        fields = ['id', 'user', 'department', 'subject', 'message', 'file']

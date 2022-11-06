from rest_framework import serializers
from .models import Ticket, Department


class DepartmentSerializers(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'title']


class TicketReadSerializer(serializers.ModelSerializer):
    department = DepartmentSerializers()

    class Meta:
        model = Ticket
        fields = ['id', 'user', 'department', 'subject', 'message', 'file']


class TicketSerializer(serializers.ModelSerializer):
    subject = serializers.CharField(required=True, max_length=256)
    message = serializers.CharField(required=True)

    class Meta:
        model = Ticket
        fields = ['id', 'user', 'department', 'subject', 'message', 'file']

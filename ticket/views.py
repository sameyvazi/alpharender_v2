from rest_framework import viewsets, permissions
from ticket.serializers import TicketSerializer, TicketReadSerializer
from .models import Ticket
from django.db.models import Q


class TicketViewSet(viewsets.ModelViewSet):
    # queryset = Ticket.objects.filter(Q(status=Ticket.STATUS_OPEN) | Q(status=Ticket.STATUS_PENDING))
    queryset = Ticket.objects.select_related('department').all()
    http_method_names = ['get', 'post']

    def get_serializer_class(self):
        if self.request.method not in permissions.SAFE_METHODS:
            return TicketSerializer
        else:
            return TicketReadSerializer

    search_fields = ('id', 'user__id', 'department__title')
    ordering_fields = ('create_time', 'modified_time')

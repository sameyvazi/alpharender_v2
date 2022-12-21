from django.shortcuts import render
from rest_framework import viewsets, permissions
from ticket.serializers import TicketSerializer, TicketReadSerializer
from .models import Ticket
from django.db.models import Q
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods


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

    @action(detail=False)
    def ticket_search(self, request):
        title = request.GET.get('q')
        tickets = Ticket.objects.filter(subject__icontains=title)
        context = " - ".join([f"{ticket.id}" for ticket in tickets])
        return Response(context)


@login_required()
@require_http_methods(request_method_list=['POST', 'GET'])
def test_view(request):
    context = dict()
    context['tickets'] = Ticket.objects.all()
    return render(request, 'ticket/test.html', context=context)

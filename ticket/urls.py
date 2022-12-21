from django.urls import include, path
from rest_framework import routers
from ticket import views
from ticket.views import test_view

router = routers.DefaultRouter()
router.register(r'tickets', views.TicketViewSet)

urlpatterns = [
    path('test/', test_view, name='test'),
    path('', include(router.urls)),
]

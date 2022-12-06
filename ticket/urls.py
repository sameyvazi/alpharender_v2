from django.urls import include, path
from rest_framework import routers
from ticket import views

router = routers.DefaultRouter()
router.register(r'tickets', views.TicketViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

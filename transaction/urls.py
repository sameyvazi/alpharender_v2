from django.urls import include, path
from rest_framework import routers
from transaction.views import TransactionViewSet, ReportModelViewSet

router = routers.DefaultRouter()
router.register(r'transaction', TransactionViewSet)
router.register(r'report', ReportModelViewSet)

urlpatterns = [
    path('', include(router.urls))
]

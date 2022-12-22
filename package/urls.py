from django.urls import include, path
from django.views.generic import TemplateView

from package.views import PackageView, PackageListView, PackageFormView

urlpatterns = [
    path('view/', PackageView.as_view(), name='package-view'),
    path('list/', PackageListView.as_view(), name='package-list'),
    path('form/', PackageFormView.as_view(), name='package-form'),
    path('base/', TemplateView.as_view(template_name='base.html'), name='package-view'),
]

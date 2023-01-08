from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import ListView, FormView
from rest_framework.response import Response
from django.urls import reverse_lazy

from package.forms import PackageForm
from package.models import Package


class PackageView(View):
    @method_decorator(login_required)
    def get(self, request):
        return HttpResponse('Hax')


class CustomListView(ListView):

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(is_active=True)


class PackageListView(CustomListView):
    model = Package
    template_name = 'package/list.html'

    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super().get_context_data(*args, object_list=object_list, **kwargs)
        context['cm'] = 'extra data'
        # print(context)
        return context


class PackageFormView(FormView):
    template_name = 'package/form.html'
    form_class = PackageForm
    success_url = reverse_lazy('package-list')

    def form_valid(self, form):
        # instance = form.save(commit=False)
        # instance.user = self.request.user
        form.save()
        return super().form_valid(form)

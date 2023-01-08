from django.test import TestCase
from django.urls import reverse, resolve
from package.views import PackageFormView
from django.views.generic import TemplateView


class TestUrls(TestCase):
    def test_package_form(self):
        url = reverse('package-form')
        self.assertEqual(resolve(url).func.view_class, PackageFormView)

    def test_template_view(self):
        url = reverse('package-view')
        self.assertEqual(resolve(url).func.view_class, TemplateView)

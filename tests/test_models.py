from django.test import TestCase
from package.models import Package
from model_bakery import baker


class TestPackageModel(TestCase):
    def setUp(self):
        self.package = baker.make(Package, title='diamond')

    def test_model_str(self):
        self.assertEqual(str(self.package), 'diamond')

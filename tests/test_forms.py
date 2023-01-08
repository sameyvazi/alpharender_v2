from django.test import TestCase
from package.forms import PackageForm


class TestPackageForm(TestCase):

    def setUp(self):
        self.form = PackageForm(data={
            'type': 1,
            'title': 'title',
            'machine_limit': 1,
            'pricing': 1,
            'per_second': 1,
            'priority': 1,
            'ghz': 1,
            'sort_order': 1,
            'is_unlimited': 1,
            'is_active': 1,
            'users': 1,
        })

    def test_valid_data(self):
        self.assertTrue(self.form.is_valid())

    def test_empty_data(self):
        form = PackageForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 8)

    def test_title_length(self):
        form = PackageForm(data={'title': "aaa"})
        self.assertTrue(form.has_error('title'))

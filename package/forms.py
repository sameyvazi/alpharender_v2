from django import forms
from django.core.exceptions import ValidationError

from package.models import Package


class PackageForm(forms.ModelForm):
    class Meta:
        model = Package
        fields = '__all__'

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) < 5:
            raise ValidationError("Length is < 5")

        return title

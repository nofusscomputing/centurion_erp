from django import forms
from django.db.models import Q

from app import settings

from access.models import Organization


class OrganizationForm(forms.ModelForm):

    class Meta:
        model = Organization
        fields = [
            'name',
            'slug',
        ]


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['created'] = forms.DateTimeField(
            label="Created",
            input_formats=settings.DATETIME_FORMAT,
            initial=kwargs['instance'].created,
            disabled=True,
            required=False,
        )

        self.fields['modified'] = forms.DateTimeField(
            label="Modified",
            input_formats=settings.DATETIME_FORMAT,
            initial=kwargs['instance'].modified,
            disabled=True,
            required=False,
        )

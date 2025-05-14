
from django import forms
from django.urls import reverse

from access.models.organization import Organization
from access.models.team_user import TeamUsers

from app import settings

from core.forms.common import CommonModelForm

from settings.models.external_link import ExternalLink


class ExternalLinksForm(CommonModelForm):

    prefix = 'external_links'

    class Meta:

        fields = '__all__'

        model = ExternalLink



class DetailForm(ExternalLinksForm):

    tabs: dict = {
        "details": {
            "name": "Details",
            "slug": "details",
            "sections": [
                {
                    "layout": "double",
                    "left": [
                        'organization',
                        'name',
                        'template',
                        'colour',
                        'cluster',
                        'devices'
                        'software',
                        'c_created',
                        'c_modified',
                    ],
                    "right": [
                        'model_notes',
                    ]
                }
            ]
        },
        "notes": {
            "name": "Notes",
            "slug": "notes",
            "sections": []
        },
    }


    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)


        self.fields['c_created'] = forms.DateTimeField(
            label = 'Created',
            input_formats=settings.DATETIME_FORMAT,
            disabled = True,
            initial = self.instance.created,
        )

        self.fields['c_modified'] = forms.DateTimeField(
            label = 'Modified',
            input_formats=settings.DATETIME_FORMAT,
            disabled = True,
            initial = self.instance.modified,
        )

        self.tabs['details'].update({
            "edit_url": reverse('Settings:_external_link_change', args=(self.instance.pk,))
        })

        self.url_index_view = reverse('Settings:External Links')

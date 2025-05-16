
from django import forms
from django.urls import reverse

from django.conf import settings

from itim.models.services import Port

from core.forms.common import CommonModelForm

from settings.models.user_settings import UserSettings



class PortForm(CommonModelForm):


    class Meta:

        fields = '__all__'

        model = Port

    prefix = 'port'



class DetailForm(PortForm):

    tabs: dict = {
        "details": {
            "name": "Details",
            "slug": "details",
            "sections": [
                {
                    "layout": "double",
                    "left": [
                        'number',
                        'description',
                        'protocol',
                        'organization',
                        'c_created',
                        'c_modified',
                        'lastinventory',
                    ],
                    "right": [
                        'model_notes',
                    ]
                }
            ]
        },
        "services": {
            "name": "Services",
            "slug": "services",
            "sections": []
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
            "edit_url": reverse('Settings:_port_change', args=(self.instance.pk,))
        })

        self.url_index_view = reverse('Settings:_ports')

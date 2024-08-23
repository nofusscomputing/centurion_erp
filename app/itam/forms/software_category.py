from django import forms
from django.urls import reverse

from app import settings

from core.forms.common import CommonModelForm

from itam.models.software import SoftwareCategory

from settings.forms.admin_settings_global import AdminGlobalModels



class SoftwareCategoryForm(
    AdminGlobalModels,
    CommonModelForm
):

    class Meta:

       fields = [
        'name',
        'slug',
        'id',
        'organization',
        'is_global',
        'model_notes',
       ]

       model = SoftwareCategory



class DetailForm(SoftwareCategoryForm):

    tabs: dict = {
        "details": {
            "name": "Details",
            "slug": "details",
            "sections": [
                {
                    "layout": "double",
                    "left": [
                        'name',
                        'slug',
                        'organization',
                        'is_global',
                        'c_created',
                        'c_modified',
                    ],
                    "right": [
                        'model_notes',
                    ]
                }
            ]
        },
        # "notes": {
        #     "name": "Notes",
        #     "slug": "notes",
        #     "sections": []
        # },
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
            "edit_url": reverse('Settings:_software_category_change', args=(self.instance.pk,))
        })

        self.url_index_view = reverse('Settings:_software_categories')

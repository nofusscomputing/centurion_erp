from django.db import models

from itam.models.device_common import DeviceCommonFieldsName

from access.models.tenancy import TenancyObject

from core.mixin.history_save import SaveHistory
from core.models.manufacturer import Manufacturer

from settings.models.app_settings import AppSettings



class DeviceModel(DeviceCommonFieldsName, SaveHistory):


    class Meta:

        ordering = [
            'manufacturer',
            'name',
        ]

        verbose_name = 'Device Model'

        verbose_name_plural = 'Device Models'


    manufacturer = models.ForeignKey(
        Manufacturer,
        blank= True,
        default = None,
        help_text = 'Manufacturer this model is from',
        null = True,
        on_delete=models.SET_DEFAULT,
        verbose_name = 'Manufacturer'
    )

    page_layout: dict = [
        {
            "name": "Details",
            "slug": "details",
            "sections": [
                {
                    "layout": "double",
                    "left": [
                        'organization',
                        'manufacturer',
                        'name',
                        'is_global',
                    ],
                    "right": [
                        'model_notes',
                        'created',
                        'modified',
                    ]
                }
            ]
        },
        {
            "name": "Knowledge Base",
            "slug": "kb_articles",
            "sections": [
                {
                    "layout": "table",
                    "field": "knowledge_base",
                }
            ]
        },
        {
            "name": "Notes",
            "slug": "notes",
            "sections": []
        }
    ]

    table_fields: list = [
        'manufacturer',
        'name',
        'organization',
        'created',
        'modified'
    ]


    def clean(self):

        app_settings = AppSettings.objects.get(owner_organization=None)

        if app_settings.device_model_is_global:

            self.organization = app_settings.global_organization
            self.is_global = app_settings.device_model_is_global


    def __str__(self):

        if self.manufacturer:

            return self.manufacturer.name + ' ' + self.name

        return self.name

    def save_history(self, before: dict, after: dict) -> bool:

        from itam.models.device_model_history import DeviceModelHistory

        history = super().save_history(
            before = before,
            after = after,
            history_model = DeviceModelHistory
        )


        return history

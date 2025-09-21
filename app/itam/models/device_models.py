from django.db import models

from access.fields import AutoLastModifiedField

from core.models.centurion import CenturionModel

from core.models.manufacturer import Manufacturer

from settings.models.app_settings import AppSettings



class DeviceModel(
    CenturionModel
):

    model_tag = 'device_model'


    class Meta:

        ordering = [
            'manufacturer',
            'name',
        ]

        verbose_name = 'Device Model'

        verbose_name_plural = 'Device Models'


    name = models.CharField(
        blank = False,
        help_text = 'The items name',
        max_length = 50,
        unique = True,
        verbose_name = 'Name'
    )

    manufacturer = models.ForeignKey(
        Manufacturer,
        blank = True,
        help_text = 'Manufacturer this model is from',
        null = True,
        on_delete = models.PROTECT,
        verbose_name = 'Manufacturer'
    )

    modified = AutoLastModifiedField()

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

        super().clean()


    def __str__(self):

        if self.manufacturer:

            return self.manufacturer.name + ' ' + self.name

        return self.name

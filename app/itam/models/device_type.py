

from django.conf import settings

from django.db import models

from access.fields import AutoLastModifiedField

from core.models.centurion import CenturionModel

from settings.models.app_settings import AppSettings



class DeviceType(
    CenturionModel,
):

    model_tag = 'device_type'

    class Meta:

        ordering = [
            'name'
        ]

        verbose_name = 'Device Type'

        verbose_name_plural = 'Device Types'


    name = models.CharField(
        blank = False,
        help_text = 'The items name',
        max_length = 50,
        unique = True,
        verbose_name = 'Name'
    )

    modified = AutoLastModifiedField()

    page_layout: dict = {
        "dataset": {
            "columns": [
                [
                    'name',
                    'organization',
                    'created',
                    'modified'
                ]
            ]
        },
        "detail": [
            {
                "name": "Details",
                "slug": "details",
                "sections": [
                    {
                        "layout": "double",
                        "left": [
                            'organization',
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
            },
        ],
        "table": [
            'name',
            'organization',
            'created',
            'modified'
        ]
    }


    def clean(self):

        app_settings = AppSettings.objects.get(owner_organization=None)

        if app_settings.device_type_is_global:

            self.organization = app_settings.global_organization

        super().clean()


    def __str__(self):

        return self.name

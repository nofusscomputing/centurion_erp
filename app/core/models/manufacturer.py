from django.db import models

from access.fields import AutoLastModifiedField

from core.models.centurion import CenturionModel

from settings.models.app_settings import AppSettings


#
# Depreciated:
#    - Migrated: https://github.com/nofusscomputing/centurion_erp/issues/914
#    - Removal: https://github.com/nofusscomputing/centurion_erp/issues/1049
#
class Manufacturer(
    CenturionModel,
):

    model_tag = 'manufacturer'


    class Meta:

        ordering = [
            'name'
        ]

        verbose_name = 'Manufacturer'

        verbose_name_plural = 'Manufacturers'


    name = models.CharField(
        blank = False,
        help_text = 'Name of this manufacturer',
        max_length = 50,
        unique = True,
        verbose_name = 'Name'
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
    ]


    table_fields: list = [
        'name',
        'organization',
        'created',
        'modified'
    ]


    def clean(self):

        app_settings = AppSettings.objects.get(owner_organization=None)

        if app_settings.manufacturer_is_global:

            self.organization = app_settings.global_organization

        super().clean()

    def __str__(self):

        return self.name

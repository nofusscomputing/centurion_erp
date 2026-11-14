from django.db import models

from access.fields import AutoLastModifiedField
from access.models.company_base import Company


from core.models.centurion import CenturionModel

from settings.models.app_settings import AppSettings



class SoftwareCategory(
    CenturionModel,
):

    model_tag = 'software_category'


    class Meta:

        ordering = [
            'name',
        ]

        verbose_name = 'Software Category'

        verbose_name_plural = 'Software Categories'


    name = models.CharField(
        blank = False,
        help_text = 'Name of this item',
        max_length = 50,
        unique = True,
        verbose_name = 'Name'
    )

    modified = AutoLastModifiedField()


    page_layout: dict = {
        "dataset": {
            "columns": [
                [
                    "name",
                    "organization",
                    "created",
                    "modified",
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
            }
        ],
        "table": [
            "name",
            "organization",
            "created",
            "modified",
        ]
    }


    def __str__(self):

        return self.name


    def clean(self):

        app_settings = AppSettings.objects.get(owner_organization=None)

        if app_settings.software_categories_is_global:

            self.organization = app_settings.global_organization

        super().clean()

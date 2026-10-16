from django.db import models

from . import ITAMAssetBase



class ITAssetOperatingSystem(
    ITAMAssetBase,
):

    model_tag = 'operating_system'

    class Meta:

        ordering = [
            'name'
        ]

        verbose_name = 'Operating System'

        verbose_name_plural = 'Operating Systems'


    publisher = models.ForeignKey(
        to = 'access.Company',
        blank = True,
        help_text = 'Who publishes this Operating System',
        null = True,
        on_delete = models.PROTECT,
        related_name = 'operating_system',
        verbose_name = 'Publisher'
    )

    name = models.CharField(
        blank = False,
        help_text = 'Name of this item',
        max_length = 50,
        unique = True,
        verbose_name = 'Name'
    )


    page_layout: dict = {
        "dataset": {
            "columns": [
                [
                    'name',
                    'publisher',
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
                            'publisher',
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
                "name": "Versions",
                "slug": "version",
                "sections": [
                    {
                        "layout": "table",
                        "field": "version",
                    }
                ]
            },
            {
                "name": "Installations",
                "slug": "installs",
                "sections": [
                    {
                        "layout": "table",
                        "field": "installations",
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
                "name": "Tickets",
                "slug": "ticket",
                "sections": [
                    {
                        "layout": "table",
                        "field": "tickets",
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
            'publisher',
            'organization',
            'created',
            'modified'
        ]
    }


    def __str__(self):

        return self.name

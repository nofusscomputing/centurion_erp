from django.db import models

from settings.models.app_settings import AppSettings

from .itam_asset_base import ITAMAssetBase
from .software import SoftwareCategory, SoftwareVersion



class ITAssetSoftware(
    ITAMAssetBase,
):

    model_tag = 'software'


    class Meta:

        ordering = [
            'name',
            'publisher__name'
        ]

        verbose_name = 'IT Asset Software'

        verbose_name_plural = 'IT Asset Softwares'


    publisher = models.ForeignKey(
        to = "access.Company",
        blank = True,
        help_text = 'Who publishes this software',
        null = True,
        on_delete = models.PROTECT,
        related_name = 'software',
        verbose_name = 'Publisher',
    )

    name = models.CharField(
        blank = False,
        help_text = 'Name of this item',
        max_length = 50,
        unique = True,
        verbose_name = 'Name'
    )

    category = models.ForeignKey(
        to = "itam.SoftwareCategory",
        blank = True,
        help_text = 'Category of this Softwarae',
        null = True,
        on_delete = models.PROTECT,
        verbose_name = 'software'

    )


    page_layout: dict = {
        "dataset": {
            "columns": [
                [
                    "name",
                    "publisher",
                    "category",
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
                            'publisher',
                            'name',
                            'category',
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
            # {
            #     "name": "Licences",
            #     "slug": "licence",
            #     "sections": [
            #         {
            #             "layout": "table",
            #             "field": "licences",
            #         }
            #     ],
            # },
            {
                "name": "Installations",
                "slug": "installs",
                "sections": [
                    {
                        "layout": "table",
                        "field": "installations",
                    }
                ],
            },
            {
                "name": "Feature Flagging",
                "slug": "feature_flagging",
                "sections": [
                    {
                        "layout": "table",
                        "field": "feature_flagging",
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
                "slug": "tickets",
                "sections": [
                    {
                        "layout": "table",
                        "field": "tickets",
                    }
                ],
            },
            {
                "name": "Notes",
                "slug": "notes",
                "sections": []
            }
        ],
        "table": [
            "name",
            "publisher",
            "category",
            "organization",
            "created",
            "modified",
        ]
    }


    def __str__(self):

        return self.name


    def clean(self):

        # Set asset_type = 'intangible'

        app_settings = AppSettings.objects.get(owner_organization=None)

        if app_settings.software_is_global:

            self.organization = app_settings.global_organization

        super().clean()

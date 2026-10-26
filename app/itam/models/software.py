from django.db import models

from access.fields import AutoLastModifiedField
from access.models.company_base import Company
from access.models.tenant import Tenant

from centurion.lib.decorators import depreciate

from core.models.centurion import CenturionModel
from core.models.manufacturer import Manufacturer

from settings.models.app_settings import AppSettings



@depreciate(
    depreciated_in = '1.36.0',
    removed_in = '2.0',
    replacement = 'itam.ITAssetSoftware',
    skip_tests = True,
)
class Software(
    CenturionModel,
):    # pragma: no cover

    model_tag = 'software'


    class Meta:

        ordering = [
            'name',
            'publisher__name'
        ]

        verbose_name = 'Software'

        verbose_name_plural = 'Softwares'


    organization = models.ForeignKey(
        to = 'access.Tenant',
        blank = False,
        help_text = 'Tenant this belongs to',
        null = True,
        on_delete = models.CASCADE,
        related_name = 'software',
        validators = [
            CenturionModel.validatate_organization_exists
        ],
        verbose_name = 'Tenant'
    )

    publisher_old = models.ForeignKey(
        to = 'core.Manufacturer',
        blank= True,
        help_text = 'Who publishes this software',
        null = True,
        on_delete = models.PROTECT,
        related_name = '+',
        verbose_name = 'Publisher',
    )

    publisher = models.ForeignKey(
        to = 'access.Company',
        blank= True,
        help_text = 'Who publishes this software',
        null = True,
        on_delete = models.PROTECT,
        related_name = '+',
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
        to = 'itam.SoftwareCategory',
        blank = True,
        help_text = 'Category of this Softwarae',
        null = True,
        on_delete = models.PROTECT,
        verbose_name = 'Category'

    )

    modified = AutoLastModifiedField()


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

        app_settings = AppSettings.objects.get(owner_organization=None)

        if app_settings.software_is_global:

            self.organization = app_settings.global_organization

        super().clean()

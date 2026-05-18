from django.apps import apps
from django.db import models

from access.fields import AutoLastModifiedField

from core.models.centurion import CenturionModel



class AssetBase(
    CenturionModel,
):
    """Asset Base Model

    This model forms the base of ALL asset models and contains the core
    features for all sub-models.

    **Don't** use this model directly, it should be used via a sub-model.
    """

    app_namespace = 'accounting'

    model_tag = 'asset'

    url_model_name = 'asset'


    @property
    def _base_model(self):

        return AssetBase


    class Meta:

        ordering = [
            'id'
        ]


        verbose_name = "Asset"

        verbose_name_plural = "Assets"


    def validate_not_null(field):

        if field is None:

            return False

        return True


    asset_number = models.CharField(
        blank = True,
        help_text = 'Number or tag to use to track this asset',
        max_length = 30,
        null = True,
        unique = True,
        verbose_name = 'Asset Number',
    )

    serial_number = models.CharField(
        blank = True,
        help_text = 'Serial number of this asset assigned by manufacturer.',
        max_length = 30,
        null = True,
        unique = True,
        verbose_name = 'Serial Number',
    )


    # category = models.ForeignKey(
    #     TicketCategory,
    #     blank = False,
    #     help_text = 'Category for this asset',
    #     on_delete = models.PROTECT,
    #     verbose_name = 'Category',
    # )
    """Category & Subcategory: Assets are grouped into broad categories like IT
    equipment, vehicles, furniture, or heavy machinery, with further 
    subcategorization to increase granularity. This classification 
    facilitates reporting, lifecycle planning, and policy enforcement for 
    different asset types.
    """


    # Status

    # model (manufacturer / model)


    modified = AutoLastModifiedField()


    page_layout: dict = {
        "dataset": {
            "columns": [
                [
                    "display_name",
                    'asset_number',
                    'serial_number',
                    'organization',
                    'created'
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
                            'asset_number',
                            'serial_number',
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
            },
        ],
        "table": [
            'id',
            {
                "field": "display_name",
                "type": "link",
                "key": "_self"
            },
            'asset_number',
            'serial_number',
            'organization',
            'created'
        ]
    }



    def __str__(self):

        return self._meta.verbose_name + ' - ' + self.asset_number

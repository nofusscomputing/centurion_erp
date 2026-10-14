from django.apps import apps
from django.conf import settings
from django.db import models

from rest_framework.reverse import reverse

from accounting.models.asset_base import AssetBase



class ITAMAssetBase(
    AssetBase,
):
    """IT Asset Base Model

    This model forms the base of ALL IT asset models and contains the core
    features for all sub-models.

    **Don't** use this model directly, it should be used via a sub-model.
    """

    _is_submodel = True

    app_namespace = 'accounting'

    url_model_name = 'asset'


    class Meta:

        ordering = [
            'id'
        ]

        verbose_name = "IT Asset Base"

        verbose_name_plural = "IT Assets Base"



    page_layout: dict = {
        "dataset": {
            "columns": [
                [
                    {
                        "field": "display_name",
                        "type": "link",
                        "key": "_self"
                    },
                    'id',
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

        if not self.asset_number:

            return self._meta.verbose_name


        return self._meta.verbose_name + ' - ' + self.asset_number

from django.conf import settings
from django.db import models

from access.fields import (
    AutoCreatedField,
    AutoLastModifiedField,
)

from core.mixins.centurion import Centurion



class Tenant(
    Centurion,
):

    @property
    def organization(self):
        return self

    model_tag = 'tenant'

    class Meta:

        verbose_name = "Tenant"

        verbose_name_plural = "Tenants"

        ordering = [
            'name'
        ]


    id = models.AutoField(
        blank = False,
        help_text = 'ID of this item',
        primary_key = True,
        unique = True,
        verbose_name = 'ID'
    )

    name = models.CharField(
        blank = False,
        help_text = 'Name of this Tenancy',
        max_length = 50,
        unique = True,
        verbose_name = 'Name'
    )

    manager = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank = True,
        help_text = 'Manager for this Tenancy',
        null = True,
        on_delete = models.PROTECT,
        verbose_name = 'Manager'
    )

    model_notes = models.TextField(
        blank = True,
        help_text = 'Tid bits of information',
        null = True,
        verbose_name = 'Notes',
    )


    created = AutoCreatedField()

    modified = AutoLastModifiedField()


    def __int__(self):

        return self.id


    def __str__(self):
        return self.name


    def get_organization(self):
        return self


    table_fields: list = [
        'nbsp',
        'name',
        'created',
        'modified',
        'nbsp'
    ]

    page_layout: list = [
        {
            "name": "Details",
            "slug": "details",
            "sections": [
                {
                    "layout": "double",
                    "left": [
                        'name',
                        'manager',
                        'created',
                        'modified',
                    ],
                    "right": [
                        'model_notes',
                    ]
                }
            ]
        },
        {
            "name": "Teams",
            "slug": "teams",
            "sections": [
                {
                    "layout": "table",
                    "field": "teams"
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



Organization = Tenant

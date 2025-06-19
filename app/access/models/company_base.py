from django.db import models

from access.models.entity import Entity



class Company(
    Entity
):
# This model is intended to be called `Organization`, however at the time of
# creation this was not possible as Tenant (ne Organization) still has
# references in code to `organization` witch clashes with the intended name of
# this model.

    _is_submodel = True

    documentation = ''


    class Meta:

        ordering = [
            'name',
        ]

        sub_model_type = 'company'

        verbose_name = 'Company'

        verbose_name_plural = 'Companies'


    name = models.CharField(
        blank = False,
        help_text = 'The name of this entity',
        max_length = 80,
        unique = False,
        verbose_name = 'Name'
    )


    def __str__(self) -> str:

        return self.name


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
            "name": "Tickets",
            "slug": "tickets",
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
    ]

    table_fields: list = [
        'name',
        'organization',
        'created',
    ]

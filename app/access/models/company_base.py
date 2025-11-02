from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

from access.models.entity import Entity

from settings.models.app_settings import AppSettings



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


    def __str__(self) -> str:

        return self.name


    def clean_fields(self, exclude = None):

        app_settings = AppSettings.objects.get(owner_organization=None)

        if app_settings.manufacturer_is_global:

            if app_settings.global_organization is None:

                log = self.context['logger']
                if log:

                    log.error(
                        msg = 'No Global organization is set, unable to save Company as a global company.'
                    )

                raise ValidationError(
                    message = {
                        'organization': ValidationError(
                            message='No global organization has been set. Please notify the webmaster.',
                            code = 'no_global_org_set'
                        )
                    },
                )

            self.organization = app_settings.global_organization

        super().clean_fields( exclude = exclude )

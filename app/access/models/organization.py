import django

from django.conf import settings
from django.db import models

from rest_framework.reverse import reverse

from access.fields import (
    AutoCreatedField,
    AutoLastModifiedField,
    AutoSlugField
)

from core.mixin.history_save import SaveHistory

User = django.contrib.auth.get_user_model()



class Organization(SaveHistory):

    class Meta:
        verbose_name = "Organization"
        verbose_name_plural = "Organizations"
        ordering = ['name']

    def save(self, *args, **kwargs):

        if self.slug == '_':
            self.slug = self.name.lower().replace(' ', '_')

        super().save(*args, **kwargs)

    id = models.AutoField(
        blank=False,
        help_text = 'ID of this item',
        primary_key=True,
        unique=True,
        verbose_name = 'ID'
    )

    name = models.CharField(
        blank = False,
        help_text = 'Name of this Organization',
        max_length = 50,
        unique = True,
        verbose_name = 'Name'
    )

    manager = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank = False,
        help_text = 'Manager for this organization',
        null = True,
        on_delete=models.SET_NULL,
        verbose_name = 'Manager'
    )

    model_notes = models.TextField(
        blank = True,
        default = None,
        help_text = 'Tid bits of information',
        null= True,
        verbose_name = 'Notes',
    )

    slug = AutoSlugField()

    created = AutoCreatedField()

    modified = AutoLastModifiedField()


    def get_organization(self):
        return self

    def __int__(self):

        return self.id

    def __str__(self):
        return self.name

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


    def get_url( self, request = None ) -> str:

        if request:

            return reverse("v2:_api_v2_organization-detail", request=request, kwargs={'pk': self.id})

        return reverse("v2:_api_v2_organization-detail", kwargs={'pk': self.id})


    def save_history(self, before: dict, after: dict) -> bool:

        from access.models.organization_history import OrganizationHistory

        history = super().save_history(
            before = before,
            after = after,
            history_model = OrganizationHistory
        )


        return history

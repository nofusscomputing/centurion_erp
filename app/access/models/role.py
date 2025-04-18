from django.contrib.auth.models import Permission
from django.db import models

from access.fields import AutoCreatedField, AutoLastModifiedField
from access.models.tenancy import TenancyObject



class Role(
    TenancyObject
):


    class Meta:

        ordering = [
            'organization',
            'name',
        ]

        unique_together = [
            'organization',
            'name'
        ]

        verbose_name = 'Role'

        verbose_name_plural = 'Roles'


    id = models.AutoField(
        blank=False,
        help_text = 'Primary key of the entry',
        primary_key=True,
        unique=True,
        verbose_name = 'ID'
    )

    name = models.CharField(
        blank = False,
        help_text = 'Name of this role',
        max_length = 30,
        unique = False,
        verbose_name = 'Name'
    )

    permissions = models.ManyToManyField(
        Permission,
        blank = True,
        help_text = 'Permissions part of this role',
        related_name = 'roles',
        symmetrical = False,
        verbose_name = 'Permissions'
    )

    created = AutoCreatedField()

    modified = AutoLastModifiedField()

    is_global = None



    def __str__(self) -> str:
        
        return str( self.organization ) + ' / ' + self.name


    documentation = ''

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
                        'created',
                        'modified',
                    ],
                    "right": [
                        'model_notes',
                    ]
                },
                {
                    "layout": "single",
                    "name": "Permissions",
                    "fields": [
                        "permissions",
                    ]
                },
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
    ]


    table_fields: list = [
        'organization',
        'name',
        'created',
        'modified',
    ]


    def save_history(self, before: dict, after: dict) -> bool:

        from access.models.role_history import RoleHistory

        history = super().save_history(
            before = before,
            after = after,
            history_model = RoleHistory
        )

        return history

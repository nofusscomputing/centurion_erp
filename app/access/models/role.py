from django.contrib.auth.models import Permission
from django.db import models

from access.fields import AutoLastModifiedField

from core.models.centurion import CenturionModel



class Role(
    CenturionModel
):

    documentation = ''

    model_tag = 'role'


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

    modified = AutoLastModifiedField()



    def __str__(self) -> str:

        return str( self.organization ) + ' / ' + self.name


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


    _permissions: list[ Permission ] = None

    _permissions_int: list[ int ] = None

    def get_permissions(self, as_int_list = False ):

        if self._permissions is None:

            permissions = []
            permissions_int = []

            for permission in self.permissions:    # pylint: disable=E1133:not-an-iterable

                if permission in _permissions:
                    continue

                permissions += [ permission ]
                permissions_int += [ permission.id ]

            self._permissions = permissions
            self._permissions_int = permissions_int

        if as_int_list:
            return self._permissions_int

        return self._permissions_int

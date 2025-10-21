from django.db import models

from access.fields import AutoLastModifiedField

from access.models.company_base import Company

from core.models.centurion import CenturionModel
from core.models.manufacturer import Manufacturer



class OperatingSystem(
    CenturionModel
):

    model_tag = 'operating_system'

    class Meta:

        ordering = [
            'name'
        ]

        verbose_name = 'Operating System'

        verbose_name_plural = 'Operating Systems'


    publisher_old = models.ForeignKey(
        Manufacturer,
        blank = True,
        help_text = 'Who publishes this Operating System',
        null = True,
        on_delete = models.PROTECT,
        verbose_name = 'Publisher'
    )

    publisher = models.ForeignKey(
        Company,
        blank = True,
        help_text = 'Who publishes this Operating System',
        null = True,
        on_delete = models.PROTECT,
        related_name = 'operating_system',
        verbose_name = 'Publisher'
    )

    name = models.CharField(
        blank = False,
        help_text = 'Name of this item',
        max_length = 50,
        unique = True,
        verbose_name = 'Name'
    )

    modified = AutoLastModifiedField()


    page_layout: dict = [
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
        #             "field": "licence",
        #         }
        #     ]
        # },
        {
            "name": "Installations",
            "slug": "installs",
            "sections": [
                {
                    "layout": "table",
                    "field": "installations",
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
            "slug": "ticket",
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
        'publisher',
        'organization',
        'created',
        'modified'
    ]


    def __str__(self):

        return self.name



class OperatingSystemVersion(
    CenturionModel
):

    model_tag = 'operating_system_version'


    class Meta:

        ordering = [
            'name',
        ]

        verbose_name = 'Operating System Version'

        verbose_name_plural = 'Operating System Versions'


    operating_system = models.ForeignKey(
        OperatingSystem,
        help_text = 'Operating system this version applies to',
        on_delete = models.PROTECT,
        verbose_name = 'Operating System'
    )

    name = models.CharField(
        blank = False,
        help_text = 'Major version number for the Operating System',
        max_length = 50,
        unique = False,
        verbose_name = 'Major Version',
    )

    modified = AutoLastModifiedField()


    page_layout: list = [
        {
            "name": "Details",
            "slug": "details",
            "sections": [
                {
                    "layout": "double",
                    "left": [
                        'organization',
                        'operating_system',
                        'name',
                        'created',
                        'modified',
                    ],
                    "right": [
                        'model_notes',
                    ]
                },
            ]
        },
        {
            "name": "Tickets",
            "slug": "tickets",
            "sections": [
                # {
                #     "layout": "table",
                #     "field": "tickets",
                # }
            ],
        },
        {
            "name": "Notes",
            "slug": "notes",
            "sections": []
        },


    ]

    table_fields: list = [
        'name',
        'installations',
        'created',
        'modified',
    ]


    def get_url_kwargs(self, many = False ) -> dict:

        kwargs = super().get_url_kwargs( many = many )

        kwargs.update({
            'operating_system_id': self.operating_system.id,
        })

        return kwargs


    def __str__(self):

        return self.operating_system.name + ' ' + self.name

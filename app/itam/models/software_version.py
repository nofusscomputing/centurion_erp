from django.db import models

from access.fields import AutoLastModifiedField

from core.models.centurion import CenturionModel



class SoftwareVersions(
    CenturionModel
):

    model_tag = 'software_version'


    class Meta:

        ordering = [
            'name'
        ]

        verbose_name = 'Software Version'

        verbose_name_plural = 'Software Versions'


    name = models.CharField(
        blank = False,
        help_text = 'Name of for the software version',
        max_length = 50,
        unique = False,
        verbose_name = 'Name'
    )

    software = models.ForeignKey(
        to = 'itam.itassetsoftware',
        blank = False,
        help_text = 'Software this version applies',
        null = False,
        on_delete = models.CASCADE,
        verbose_name = 'versions',
    )

    modified = AutoLastModifiedField()


    page_layout: dict = {
        "dataset": {
            "columns": [
                [
                    'name',
                    'organization',
                    'created',
                    'modified',
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
                            'software',
                            'name',
                            'created',
                            'modified',
                        ],
                        "right": [
                            'model_notes',
                            'is_virtual',
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

        ],
        "table": [
            'name',
            'organization',
            'created',
            'modified',
        ]
    }


    def get_url_kwargs(self, many = False) -> dict:

        kwargs = super().get_url_kwargs( many = many)

        kwargs.update({
            'software_id': self.software.id,
        })

        return kwargs


    def __str__(self):

        return self.software.name + ' ' + self.name



class SoftwareVersion(
    CenturionModel
):

    model_tag = 'software_version'


    class Meta:

        ordering = [
            'name'
        ]

        verbose_name = 'Software Version'

        verbose_name_plural = 'Software Versions'


    software = models.ForeignKey(
        to = 'itam.Software',
        blank = False,
        help_text = 'Software this version applies',
        null = False,
        on_delete = models.CASCADE,
        related_name = 'versions',
        verbose_name = 'Software',
    )

    name = models.CharField(
        blank = False,
        help_text = 'Name of for the software version',
        max_length = 50,
        unique = False,
        verbose_name = 'Name'
    )

    modified = AutoLastModifiedField()


    page_layout: dict = {
        "dataset": {
            "columns": [
                [
                    'name',
                    'organization',
                    'created',
                    'modified',
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
                            'software',
                            'name',
                            'created',
                            'modified',
                        ],
                        "right": [
                            'model_notes',
                            'is_virtual',
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

        ],
        "table": [
            'name',
            'organization',
            'created',
            'modified',
        ]
    }


    def get_url_kwargs(self, many = False) -> dict:

        kwargs = super().get_url_kwargs( many = many)

        kwargs.update({
            'software_id': self.software.id,
        })

        return kwargs


    def __str__(self):

        return self.software.name + ' ' + self.name

from django.db import models

from access.fields import AutoLastModifiedField

from core.models.centurion import CenturionModel



class ExternalLink(
    CenturionModel
):


    class Meta:

        ordering = [
            'name',
            'organization',
        ]

        verbose_name = 'External Link'

        verbose_name_plural = 'External Links'


    name = models.CharField(
        blank = False,
        help_text = 'Name to display on link button',
        max_length = 30,
        unique = True,
        verbose_name = 'Friendly Name',
    )

    button_text = models.CharField(
        blank = True,
        help_text = 'Name to display on link button',
        max_length = 30,
        null = True,
        unique = True,
        verbose_name = 'Button Text',
    )

    template = models.CharField(
        blank = False,
        help_text = 'External Link template',
        max_length = 180,
        unique = False,
        verbose_name = 'Link Template',
    )

    colour = models.CharField(
        blank = True,
        help_text = 'Colour to render the link button. Use HTML colour code',
        max_length = 80,
        null = True,
        unique = False,
        verbose_name = 'Button Colour',
    )

    cluster = models.BooleanField(
        blank = False,
        default = False,
        help_text = 'Render link for clusters',
        verbose_name = 'Clusters',
    )

    devices = models.BooleanField(
        blank = False,
        default = False,
        help_text = 'Render link for devices',
        verbose_name = 'Devices',
    )

    service = models.BooleanField(
        blank = False,
        default = False,
        help_text = 'Render link for service',
        verbose_name = 'Service',
    )

    software = models.BooleanField(
        blank = False,
        default = False,
        help_text = 'Render link for software',
        verbose_name = 'Software',
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
                        'name',
                        'button_text',
                        'template',
                        'colour',
                    ],
                    "right": [
                        'model_notes',
                        'created',
                        'modified',
                    ]
                },
                {
                    "name": "Assignable to",
                    "layout": "double",
                    "left": [
                        'cluster',
                        'service',
                    ],
                    "right": [
                        'devices',
                        'software',
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
            "name": "Notes",
            "slug": "notes",
            "sections": []
        },
    ]


    table_fields: list = [
        'name',
        'organization',
        'created',
        'modified'
    ]


    def __str__(self):
        """ Return the Template to render """

        return str(self.template)

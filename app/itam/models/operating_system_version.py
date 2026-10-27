from django.db import models

from access.fields import AutoLastModifiedField

from core.models.centurion import CenturionModel



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
        to = 'itam.OperatingSystem',
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


    page_layout: dict = {
        "detail": [
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


        ],
        "dataset": {
            "columns": [
                [
                    'name',
                    'created',
                    'modified',
                ]
            ]
        },
        "table": [
            'name',
            'created',
            'modified',
        ]
    }


    def get_url_kwargs(self, many = False ) -> dict:

        kwargs = super().get_url_kwargs( many = many )

        kwargs.update({
            'operating_system_id': self.operating_system.id,
        })

        return kwargs


    def __str__(self):

        return self.operating_system.name + ' ' + self.name

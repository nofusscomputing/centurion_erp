from django.db import models

from access.fields import AutoLastModifiedField, AutoCreatedField, AutoSlugField
from access.models.tenancy import TenancyObject

from core.mixins.history_save import SaveHistory
from core.models.centurion import CenturionModel
from core.models.manufacturer import Manufacturer



class OperatingSystemCommonFields(TenancyObject, models.Model):

    class Meta:
        abstract = True

    id = models.AutoField(
        blank=False,
        help_text = 'ID of this item',
        primary_key=True,
        unique=True,
        verbose_name = 'ID'
    )

    created = AutoCreatedField()

    # modified = AutoLastModifiedField()



class OperatingSystemFieldsName(OperatingSystemCommonFields):

    class Meta:
        abstract = True

    # name = models.CharField(
    #     blank = False,
    #     help_text = 'Name of this item',
    #     max_length = 50,
    #     unique = True,
    #     verbose_name = 'Name'
    # )

    slug = AutoSlugField()



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


    publisher = models.ForeignKey(
        Manufacturer,
        blank = True,
        help_text = 'Who publishes this Operating System',
        null = True,
        on_delete = models.PROTECT,
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


    def get_organization(self):

        return self.organization



class OperatingSystemVersion(
    OperatingSystemCommonFields, SaveHistory
):


    class Meta:

        ordering = [
            'name',
        ]

        verbose_name = 'Operating System Version'

        verbose_name_plural = 'Operating System Versions'


    operating_system = models.ForeignKey(
        OperatingSystem,
        help_text = 'Operating system this version applies to',
        on_delete = models.CASCADE,
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


    def get_url_kwargs(self) -> dict:

        return {
            'operating_system_id': self.operating_system.id,
            'pk': self.id
        }


    def get_url_kwargs_notes(self) -> dict:
        """Fetch the URL kwargs for model notes

        Returns:
            dict: notes kwargs required for generating the URL with `reverse`
        """

        return {
            'operating_system_id': self.operating_system.id,
            'model_id': self.id
        }


    # @property
    # def parent_object(self):
    #     """ Fetch the parent object """
        
    #     return self.operating_system


    def __str__(self):

        return self.operating_system.name + ' ' + self.name

    def save_history(self, before: dict, after: dict) -> bool:

        from itam.models.operating_system_version_history import OperatingSystemVersionHistory

        history = super().save_history(
            before = before,
            after = after,
            history_model = OperatingSystemVersionHistory,
        )


        return history


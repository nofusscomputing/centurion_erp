from django.db import models

from access.fields import AutoLastModifiedField
from access.models.tenant import Tenant

from core.models.centurion import CenturionModel
from core.models.manufacturer import Manufacturer

from settings.models.app_settings import AppSettings



class SoftwareCategory(
    CenturionModel,
):

    model_tag = 'software_category'


    class Meta:

        ordering = [
            'name',
        ]

        verbose_name = 'Software Category'

        verbose_name_plural = 'Software Categories'


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
            "name": "Notes",
            "slug": "notes",
            "sections": []
        }
    ]


    table_fields: list = [
        "name",
        "organization",
        "created",
        "modified",
    ]


    def __str__(self):

        return self.name


    def clean(self):

        app_settings = AppSettings.objects.get(owner_organization=None)

        if app_settings.software_categories_is_global:

            self.organization = app_settings.global_organization



class Software(
    CenturionModel,
):

    model_tag = 'software'


    class Meta:

        ordering = [
            'name',
            'publisher__name'
        ]

        verbose_name = 'Software'

        verbose_name_plural = 'Softwares'


    organization = models.ForeignKey(
        Tenant,
        blank = False,
        help_text = 'Tenant this belongs to',
        null = False,
        on_delete = models.CASCADE,
        related_name = 'software',
        validators = [
            CenturionModel.validatate_organization_exists
        ],
        verbose_name = 'Tenant'
    )

    publisher = models.ForeignKey(
        Manufacturer,
        blank= True,
        help_text = 'Who publishes this software',
        null = True,
        on_delete = models.PROTECT,
        verbose_name = 'Publisher',
    )

    name = models.CharField(
        blank = False,
        help_text = 'Name of this item',
        max_length = 50,
        unique = True,
        verbose_name = 'Name'
    )

    category = models.ForeignKey(
        SoftwareCategory,
        blank = True,
        help_text = 'Category of this Softwarae',
        null = True,
        on_delete = models.PROTECT,
        verbose_name = 'Category'

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
                        'category',
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
        #             "field": "licences",
        #         }
        #     ],
        # },
        {
            "name": "Installations",
            "slug": "installs",
            "sections": [
                {
                    "layout": "table",
                    "field": "installations",
                }
            ],
        },
        {
            "name": "Feature Flagging",
            "slug": "feature_flagging",
            "sections": [
                {
                    "layout": "table",
                    "field": "feature_flagging",
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
            ],
        },
        {
            "name": "Notes",
            "slug": "notes",
            "sections": []
        }
    ]


    table_fields: list = [
        "name",
        "publisher",
        "category",
        "organization",
        "created",
        "modified",
    ]


    def __str__(self):

        return self.name


    def clean(self):

        app_settings = AppSettings.objects.get(owner_organization=None)

        if app_settings.software_is_global:

            self.organization = app_settings.global_organization


    def get_organization(self):
        return self.organization


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
        Software,
        blank = False,
        help_text = 'Software this version applies',
        null = False,
        on_delete = models.CASCADE,
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


    page_layout: list = [
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

    ]

    table_fields: list = [
        'name',
        'organization',
        'created',
        'modified',
    ]


    def get_url_kwargs(self, many = False) -> dict:

        kwargs = super().get_url_kwargs( many = many)

        kwargs.update({
            'software_id': self.software.id,
        })

        return kwargs


    def __str__(self):

        return self.software.name + ' ' + self.name

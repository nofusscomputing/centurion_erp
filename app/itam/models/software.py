from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver

from access.fields import *
from access.models.tenancy import Tenant, TenancyObject

from core.mixins.history_save import SaveHistory
from core.models.centurion import CenturionModel
from core.models.manufacturer import Manufacturer
from core.signal.ticket_linked_item_delete import TicketLinkedItem, deleted_model

from settings.models.app_settings import AppSettings


class SoftwareCommonFields(TenancyObject, models.Model):

    class Meta:
        abstract = True

    id = models.AutoField(
        blank=False,
        help_text = 'Id of this item',
        primary_key=True,
        unique=True,
        verbose_name = 'ID'
    )

    slug = AutoSlugField()

    created = AutoCreatedField()



class SoftwareCategory(
    SoftwareCommonFields, SaveHistory
):


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


    def clean(self):

        app_settings = AppSettings.objects.get(owner_organization=None)

        if app_settings.software_categories_is_global:

            self.organization = app_settings.global_organization


    def __str__(self):

        return self.name

    def save_history(self, before: dict, after: dict) -> bool:

        from itam.models.software_category_history import SoftwareCategoryHistory

        history = super().save_history(
            before = before,
            after = after,
            history_model = SoftwareCategoryHistory,
        )


        return history



class Software(
    CenturionModel
):

    model_tag = 'software'


    class Meta:

        ordering = [
            'name',
            'publisher__name'
        ]

        verbose_name = 'Software'

        verbose_name_plural = 'Softwares'


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
    SoftwareCommonFields, SaveHistory
):


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


    # model does not have it's own page
    # as it's a secondary model. 
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


    def get_url_kwargs(self) -> dict:

        return {
            'software_id': self.software.id,
            'pk': self.id
        }

    def get_url_kwargs_notes(self) -> dict:
        """Fetch the URL kwargs for model notes

        Returns:
            dict: notes kwargs required for generating the URL with `reverse`
        """

        return {
            'software_id': self.software.id,
            'model_id': self.id
        }


    # @property
    # def parent_object(self):
    #     """ Fetch the parent object """
        
    #     return self.software


    def __str__(self):

        return self.software.name + ' ' + self.name

    def save_history(self, before: dict, after: dict) -> bool:

        from itam.models.software_version_history import SoftwareVersionHistory

        history = super().save_history(
            before = before,
            after = after,
            history_model = SoftwareVersionHistory,
        )


        return history




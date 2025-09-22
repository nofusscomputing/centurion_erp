from django.db import models

from access.fields import AutoLastModifiedField
from access.models.tenant import Tenant

from core.models.centurion import CenturionModel



class AppSettings(
    CenturionModel,
):
    """ Application Settings

    This model is for storing settings for the application as a whole

    This class contains field `owner_organization` which exists so that in the future
    if there is a requirement for orgnizational settings, that this table can be used by
    specifying the `owner_organization`

    Raises:
        ValidationError: When software set as global and no organization has been specified 
    """

    _notes_enabled = False

    class Meta:

        ordering = [
            'owner_organization'
        ]

        verbose_name = 'App Settings'

        verbose_name_plural = 'App Settings'

    model_notes = None

    organization = None

    owner_organization = models.ForeignKey(
        Tenant,
        blank= True,
        help_text = 'Tenant the settings belong to',
        null = True,
        on_delete = models.CASCADE,
        related_name = 'owner_organization'
    )

    device_model_is_global = models.BooleanField (
        blank= False,
        help_text = 'Should Device Models be global',
        default = False,
        verbose_name = 'Global Device Models',
    )

    device_type_is_global = models.BooleanField (
        blank= False,
        help_text = 'Should Device Types be global',
        default = False,
        verbose_name = 'Global Device Types',
    )

    manufacturer_is_global = models.BooleanField (
        blank= False,
        help_text = 'Should Manufacturers / Publishers be global',
        default = False,
        verbose_name = 'Global Manufacturers / Publishers',
    )

    software_is_global = models.BooleanField (
        blank= False,
        default = False,
        help_text = 'Should Software be global',
        verbose_name = 'Global Software',
    )

    software_categories_is_global = models.BooleanField (
        blank= False,
        default = False,
        help_text = 'Should Software be global',
        verbose_name = 'Global Software Categories',
    )

    global_organization = models.ForeignKey(
        Tenant,
        on_delete = models.PROTECT,
        blank= True,
        help_text = 'Tenant global items will be created in',
        null = True,
        related_name = 'global_organization',
        verbose_name = 'Global Tenant'
    )

    modified = AutoLastModifiedField()

    table_fields: list = []

    page_layout: list = [
        {
            "name": "Details",
            "slug": "details",
            "sections": [
                {
                    "layout": "double",
                    "left": [
                        'global_organization',
                    ],
                    "right": [
                        'device_model_is_global',
                        'device_type_is_global',
                        'manufacturer_is_global',
                        'software_is_global',
                        'software_categories_is_global',

                    ]
                }
            ]
        }
    ]


    def get_tenant(self):

        return self.owner_organization


    def clean(self):
        from django.core.exceptions import ValidationError

        if self.software_is_global and self.global_organization is None:

            raise ValidationError("Global Software must have a global organization")

        super().clean()

    __all__ = [
        'device_model_is_global',
        'device_type_is_global',
        'manufacturer_is_global',
        'software_is_global',
        'software_categories_is_global',
        'global_organization',
    ]

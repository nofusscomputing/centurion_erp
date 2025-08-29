from django.conf import settings
from django.contrib.auth.models import ContentType
from django.db import models

from access.fields import *
from access.models.tenancy import TenancyObject

from core.lib.feature_not_used import FeatureNotUsed



class ModelNotes(TenancyObject):
    """ Base Notes Model
    
    Common fields for Model notes. This model must not be used directly and
    should be included in the model that contains the model fields.

    The model notes class that inherits this class must include the following
    class objects:
    
    - `get_url` or `get_url_kwargs` function
    - `model` field of type `models.ForeignKey`
    """

    class Meta:

        db_table = 'core_model_notes'

        ordering = [
            '-created'
        ]


        verbose_name = 'Model Note'

        verbose_name_plural = 'Model Notes'



    id = models.AutoField(
        blank=False,
        help_text = 'ID of this note',
        primary_key=True,
        unique=True,
        verbose_name = 'ID'
    )

    content = models.TextField(
        blank = False,
        help_text = 'The tid bit you wish to add',
        null = False,
        verbose_name = 'Note',
    )


    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank = True,
        help_text = 'User whom added the Note',
        null = False,
        on_delete=models.PROTECT,
        related_name = 'created_notes',
        verbose_name = 'Created By',
    )

    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank= True,
        default = None,
        help_text = 'User whom modified the note',
        null = True,
        on_delete=models.PROTECT,
        related_name = 'modified_notes',
        verbose_name = 'Edited By',
    )

    content_type = models.ForeignKey(
        ContentType,
        blank= True,
        help_text = 'Model this note is for',
        null = False,
        on_delete=models.CASCADE,
        verbose_name = 'Content Model'
    )

    created = AutoCreatedField(
        editable = True,
    )

    modified = AutoLastModifiedField()



    # this model is not intended to have its own viewable page as
    # it's a sub model
    page_layout: dict = []

    # This model is not expected to be viewable in a table
    # as it's a sub-model
    table_fields: list = []

    def __str__(self):

        return 'Note ' + str(self.id)


    def get_url_kwargs_notes(self):

        return FeatureNotUsed


    @property
    def parent_object(self):
        """ Fetch the parent object """
        
        return self.model

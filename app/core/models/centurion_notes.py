from django.conf import settings
from django.contrib.auth.models import ContentType
from django.db import models

from access.fields import AutoLastModifiedField
from core.models.centurion import CenturionModel



class CenturionModelNote(
    CenturionModel
):
    """ Base Centurion Notes Model"""


    class Meta:

        ordering = [
            '-created'
        ]

        verbose_name = 'Centurion Model Note'

        verbose_name_plural = 'Centurion Model Notes'


    model_notes = None


    body = models.TextField(
        blank = False,
        help_text = 'The tid bit of information you wish to add',
        null = False,
        verbose_name = 'Note',
    )


    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank = True,
        help_text = 'User whom added the Note',
        null = False,
        on_delete = models.PROTECT,
        related_name = '+',
        verbose_name = 'Created By',
    )


    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank = True,
        help_text = 'User whom modified the note',
        null = True,
        on_delete = models.PROTECT,
        related_name = '+',
        verbose_name = 'Edited By',
    )


    content_type = models.ForeignKey(
        ContentType,
        blank = True,
        help_text = 'Model this note is for',
        null = False,
        on_delete=models.CASCADE,
        verbose_name = 'Content Model'
    )


    modified = AutoLastModifiedField()


    # this model is not intended to have its own viewable page as
    # it's a sub model
    page_layout: dict = []

    # This model is not expected to be viewable in a table
    # as it's a sub-model
    table_fields: list = []

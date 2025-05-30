from django.conf import settings
from django.contrib.auth.models import ContentType
from django.core.exceptions import (
    ValidationError
)
from django.db import models

from access.fields import AutoLastModifiedField
from core.models.centurion import (
    CenturionModel,
    CenturionSubModel,
)



class CenturionModelNote(
    CenturionModel
):
    """ Base Centurion Notes Model"""

    _audit_enabled = False

    _notes_enabled = False


    @property
    def url_model_name(self):
        return CenturionModelNote._meta.model_name


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



class NoteMetaModel(
    CenturionModelNote,
    CenturionSubModel,
):

    model_notes = None

    class Meta:
        abstract = True
        proxy = False



    def clean(self):

        if not self.created_by:

            raise ValidationError(
                code = 'no_user_supplied',
                message = 'No user was supplied for this model note.'
            )

        super().clean()


    def clean_fields(self, exclude = None):

        if not getattr(self, 'model', None):

            raise ValidationError(
                code = 'no_model_supplied',
                message = 'No model was supplied for his "Model note".'
            )


        self.organization = self.model.organization

        if not self.id:

            self.created_by = self.context['user']

        else:

            self.modified_by = self.context['user']

        self.content_type = ContentType.objects.get(
            app_label = self.model._meta.app_label,
            model = self.model._meta.model_name
        )

        super().clean_fields(exclude = exclude)



    def get_url_kwargs(self):

        kwargs = {}

        kwargs.update({
            **super().get_url_kwargs(),
            'model_name': str(self._meta.model_name).replace('centurionmodelnote', ''),
        })

        return kwargs

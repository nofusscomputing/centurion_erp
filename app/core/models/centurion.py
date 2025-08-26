from django.core.exceptions import (
    ValidationError
)
from django.db import models

from access.fields import AutoCreatedField
from access.models.tenancy_abstract import TenancyAbstractModel

from core.mixins.centurion import Centurion



class CenturionModel(
    Centurion,
    TenancyAbstractModel,
):


    class Meta:

        abstract = True


    id = models.AutoField(
        blank=False,
        help_text = 'ID of the item',
        primary_key=True,
        unique=True,
        verbose_name = 'ID'
    )


    model_notes = models.TextField(
        blank = True,
        help_text = 'Tid bits of information',
        null = True,
        verbose_name = 'Notes',
    )


    created = AutoCreatedField(
        editable = True
    )


    def __int__(self) -> int:
        return int(self.id)


    @staticmethod
    def validate_field_not_none(value):

        if value is None:

            raise ValidationError(code = 'field_value_not_none', message = 'Value can not be none.')

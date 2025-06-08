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


    @staticmethod
    def validate_field_not_none(value):

        if value is None:

            raise ValidationError(code = 'field_value_not_none', message = 'Value can not be none.')



class CenturionSubModel(
    CenturionModel
):

    _is_submodel: bool = True
    """This model a sub-model"""


    class Meta:

        abstract = True


    def get_url_kwargs(self, many = False):

        kwargs = {}

        kwargs.update({
            **super().get_url_kwargs( many = many ),
            'app_label': self._meta.app_label,
            'model_name': str(self._meta.model_name),
            'model_id': self.model.id,
        })

        return kwargs

from django.conf import settings
from django.core.exceptions import (
    ValidationError
)
from django.db import models

from access.fields import AutoCreatedField

from rest_framework.reverse import reverse

from access.models.tenancy_abstract import TenancyAbstractModel



class CenturionModel(
    TenancyAbstractModel,
):



    _audit_enabled: bool = True
    """Should this model have audit history kept"""

    _is_submodel: bool = False
    """This model a sub-model"""

    _notes_enabled: bool = True
    """Should a table for notes be created for this model"""



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



    def delete(self, using = None, keep_parents = None):
        """Delete Centurion Model

        If a model has `_audit_enabled = True`, audit history is populated and
        ready to be saved by the audit system (save signal.). 

        Args:
            using (_type_, optional): _description_. Defaults to None.
            keep_parents (bool, optional): Keep parent models. Defaults to the
                value if is_submodel so as not to delete parent models.
        """

        if keep_parents is None:
            keep_parents = self._is_submodel

        if self._audit_enabled:

            self._after = {}

            self._before = type(self).objects.get( id = self.id ).get_audit_values()


        super().delete(using = using, keep_parents = keep_parents)



    def full_clean(self, exclude = None, validate_unique = True, validate_constraints = True) -> None:

        super().full_clean(
            exclude = exclude,
            validate_unique = validate_unique, 
            validate_constraints = validate_constraints
        )


    def get_audit_values(self) -> dict:
        """Retrieve the field Values

        Currently ensures only fields are present.

        **ToDo:** Update so the dict that it returns is a dict of dict where each dict
        is named after the actual models the fields come from and it contains
        only it's fields.

        Returns:
            dict: Model fields
        """

        if self.id is None:
            return {}


        data = self.__dict__.copy()

        clean_data: dict = {}

        for field in self._meta.fields:

            clean_data.update({
                field.name: getattr(self, field.name)
            })


        return clean_data



    def get_after(self) -> dict:
        """Audit Data After Change

        Returns:
            dict: All model fields after the data changed
        """
        return self._after



    def get_before(self) -> dict:
        """Audit Data Before Change

        Returns:
            dict: All model fields before the data changed
        """
        return self._before



    def get_history_model_name(self) -> str:
        """Get the name for the History Model

        Returns:
            str: Name of the history model (`<model class name>AuditHistory`)
        """
        
        return f'{self._meta.object_name}AuditHistory'



    def get_url( self, relative: bool = False, api_version: int = 2 ) -> str:
        """Return the models API URL

        Args:
            relative (bool, optional): Return the relative URL for the model. Defaults to False.
            api_version (int, optional): API Version to use. Defaults to `2``.

        Returns:
            str: API URL for the model
        """

        namespace = f'v{api_version}'

        url_basename = f'{namespace}:_api_{self._meta.model_name}-detail'

        url = reverse( viewname = url_basename, kwargs = { 'pk': self.id } )

        if not relative:

            url = settings.SITE_URL + url


        return url



    def save(self, force_insert = False, force_update = False, using = None, update_fields = None):
        """Save Centurion Model

        This Save ensures that `full_clean()` is called so that prior to the
        model being saved to the database, it is valid.

        If a model has `_audit_enabled = True`, audit history is populated and
        ready to be saved by the audit system (save signal.). 
        """

        self.full_clean(
            exclude = None,
            validate_unique = True,
            validate_constraints = True
        )

        if self._audit_enabled:

            self._after = self.get_audit_values()

            self._before = {}

            if self.id:
                
                self._before = type(self).objects.get( id = self.id ).get_audit_values()


        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)



class CenturionSubModel(
    CenturionModel
):

    _is_submodel: bool = True
    """This model a sub-model"""


    class Meta:

        abstract = True

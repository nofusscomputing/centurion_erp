from django.db import models
from django.core.exceptions import (
    ValidationError
)



class CenturionModel(
    models.Model
):



    _audit_enabled: bool = True
    """Should this model have audit history kept"""

    _is_submodel: bool = False
    """This model a sub-model"""


    class Meta:

        abstract = True


    @staticmethod
    def validate_field_not_none(value):
        
        if value is None:

            raise ValidationError(code = 'field_value_not_none', message = 'Value can not be none.')



    def get_history_model_name(self) -> str:
        """Get the name for the History Model

        Returns:
            str: Name of the history model (`<model class name>AuditHistory`)
        """
        
        return f'{self._meta.object_name}AuditHistory'


class CenturionSubModel(
    CenturionModel
):

    _is_submodel: bool = True
    """This model a sub-model"""


    class Meta:

        abstract = True

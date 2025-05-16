from django.db import models
from django.core.exceptions import (
    ValidationError
)



class CenturionModel(
    models.Model
):



    class Meta:

        abstract = True


    @staticmethod
    def validate_field_not_none(value):
        
        if value is None:

            raise ValidationError(code = 'field_value_not_none', message = 'Value can not be none.')

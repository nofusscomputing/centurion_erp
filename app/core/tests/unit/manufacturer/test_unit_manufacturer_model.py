import pytest

from django.db import models


from core.tests.unit.centurion_abstract.test_unit_centurion_abstract_model import (
    CenturionAbstractModelInheritedCases
)



@pytest.mark.model_manufacturer
class ManufacturerModelTestCases(
    CenturionAbstractModelInheritedCases
):


    @property
    def parameterized_class_attributes(self):

        return {
            'model_tag': {
                'type': str,
                'value': 'manufacturer'
            },
        }


    @property
    def parameterized_model_fields(self):
        
        return {
        'name': {
            'blank': False,
            'default': models.fields.NOT_PROVIDED,
            'field_type': models.CharField,
            'max_length': 50,
            'null': False,
            'unique': True,
        },
        'modified': {
            'blank': False,
            'default': models.fields.NOT_PROVIDED,
            'field_type': models.DateTimeField,
            'null': False,
            'unique': False,
        },
    }



class ManufacturerModelInheritedCases(
    ManufacturerModelTestCases,
):
    pass



@pytest.mark.module_core
class ManufacturerModelPyTest(
    ManufacturerModelTestCases,
):
    pass

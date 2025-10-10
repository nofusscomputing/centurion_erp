import pytest

from django.db import models


from core.tests.unit.centurion_abstract.test_unit_centurion_abstract_model import (
    CenturionAbstractTenancyModelInheritedCases
)



@pytest.mark.model_port
class PortModelTestCases(
    CenturionAbstractTenancyModelInheritedCases
):


    @property
    def parameterized_class_attributes(self):

        return {
            'model_tag': {
                'type': str,
                'value': 'port'
            },
        }


    @property
    def parameterized_model_fields(self):

        return {
        'number': {
            'blank': False,
            'default': models.fields.NOT_PROVIDED,
            'field_type': models.IntegerField,
            'null': False,
            'unique': False,
        },
        'description': {
            'blank': True,
            'default': models.fields.NOT_PROVIDED,
            'field_type': models.CharField,
            'length': 80,
            'null': True,
            'unique': False,
        },
        'protocol': {
            'blank': False,
            'default': models.fields.NOT_PROVIDED,
            'field_type': models.CharField,
            'null': False,
            'unique': False,
        },
        'modified': {
            'blank': False,
            'default': models.fields.NOT_PROVIDED,
            'field_type': models.DateTimeField,
            'null': False,
            'unique': False,
        },
    }



class PortModelInheritedCases(
    PortModelTestCases,
):
    pass



@pytest.mark.module_itim
class PortModelPyTest(
    PortModelTestCases,
):
    pass

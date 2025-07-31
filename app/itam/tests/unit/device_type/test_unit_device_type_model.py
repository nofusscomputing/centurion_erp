import pytest

from django.db import models


from core.tests.unit.centurion_abstract.test_unit_centurion_abstract_model import (
    CenturionAbstractModelInheritedCases
)



@pytest.mark.model_devicetype
class DeviceTypeModelTestCases(
    CenturionAbstractModelInheritedCases
):


    @property
    def parameterized_class_attributes(self):

        return {
            'model_tag': {
                'type': str,
                'value': 'device_type'
            },
        }


    @property
    def parameterized_model_fields(self):

        return {
        'name': {
            'blank': False,
            'default': models.fields.NOT_PROVIDED,
            'field_type': models.CharField,
            'length': 50,
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



class DeviceTypeModelInheritedCases(
    DeviceTypeModelTestCases,
):
    pass



@pytest.mark.module_itam
class DeviceTypeModelPyTest(
    DeviceTypeModelTestCases,
):
    pass

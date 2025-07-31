import pytest

from django.db import models


from core.tests.unit.centurion_abstract.test_unit_centurion_abstract_model import (
    CenturionAbstractModelInheritedCases
)



@pytest.mark.model_devicemodel
class DeviceModelModelTestCases(
    CenturionAbstractModelInheritedCases
):


    @property
    def parameterized_class_attributes(self):

        return {
            'model_tag': {
                'type': str,
                'value': 'device_model'
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
        'manufacturer': {
            'blank': True,
            'default': models.fields.NOT_PROVIDED,
            'field_type': models.ForeignKey,
            'null': True,
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


    @pytest.mark.skip(reason="to be written")
    def test_device_move_organization(user):
        """Move Organization test

        When a device moves organization, devicesoftware and devicesoftware table data
        must also move organizations
        """
        pass



class DeviceModelModelInheritedCases(
    DeviceModelModelTestCases,
):
    pass


@pytest.mark.module_itam
class DeviceModelModelPyTest(
    DeviceModelModelTestCases,
):
    pass

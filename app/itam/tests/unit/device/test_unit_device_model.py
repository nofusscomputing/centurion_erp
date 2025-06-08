import pytest

from django.db import models


from core.tests.unit.centurion_abstract.test_unit_centurion_abstract_model import (
    CenturionAbstractModelInheritedCases
)



@pytest.mark.model_gitgroup
class DeviceModelTestCases(
    CenturionAbstractModelInheritedCases
):


    @property
    def parameterized_class_attributes(self):
        
        return {
            'model_tag': {
                'type': str,
                'value': 'device'
            },
        }


    parameterized_model_fields = {
        'name': {
            'blank': False,
            'default': models.fields.NOT_PROVIDED,
            'field_type': models.IntegerField,
            'length': 50,
            'null': False,
            'unique': True,
        },
        'serial_number': {
            'blank': True,
            'default': models.fields.NOT_PROVIDED,
            'field_type': models.CharField,
            'null': True,
            'unique': True,
        },
        'uuid': {
            'blank': True,
            'default': models.fields.NOT_PROVIDED,
            'field_type': models.CharField,
            'length': 50,
            'null': True,
            'unique': True,
        },
        'device_model': {
            'blank': True,
            'default': models.fields.NOT_PROVIDED,
            'field_type': models.ForeignKey,
            'null': True,
            'unique': False,
        },
        'device_type': {
            'blank': True,
            'default': models.fields.NOT_PROVIDED,
            'field_type': models.ForeignKey,
            'null': True,
            'unique': False,
        },
        'config': {
            'blank': True,
            'default': models.fields.NOT_PROVIDED,
            'field_type': models.JSONField,
            'null': True,
            'unique': False,
        },
        'inventorydate': {
            'blank': True,
            'default': models.fields.NOT_PROVIDED,
            'field_type': models.DateTimeField,
            'null': True,
            'unique': False,
        },
        'is_virtual': {
            'blank': True,
            'default': False,
            'field_type': models.BooleanField,
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


    @pytest.mark.skip(reason="to be written")
    def test_device_move_organization(user):
        """Move Organization test

        When a device moves organization, devicesoftware and devicesoftware table data
        must also move organizations
        """
        pass



class DeviceModelInheritedCases(
    DeviceModelTestCases,
):
    pass



class DeviceModelPyTest(
    DeviceModelTestCases,
):
    pass

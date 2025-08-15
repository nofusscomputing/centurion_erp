import pytest

from django.db import models

from core.tests.unit.mixin_centurion.test_unit_centurion_mixin import (
    CenturionMixnInheritedCases,
)


@pytest.mark.module_access
@pytest.mark.model_tenant
class TenantModelTestCases(
    CenturionMixnInheritedCases
):


    @property
    def parameterized_class_attributes(self):

        return {
            'model_tag': {
                'type': str,
                'value': 'tenant'
            },
        }


    @property
    def parameterized_model_fields(self):
        
        return {
        'id': {
            'blank': True,
            'default': models.fields.NOT_PROVIDED,
            'field_type': models.AutoField,
            'null': False,
            'unique': True,
        },
        'name': {
            'blank': False,
            'default': models.fields.NOT_PROVIDED,
            'field_type': models.CharField,
            'max_length': 50,
            'null': False,
            'unique': True,
        },
        'manager': {
            'blank': True,
            'default': models.fields.NOT_PROVIDED,
            'field_type': models.ForeignKey,
            'null': True,
            'unique': False,
        },
        'model_notes': {
            'blank': True,
            'default': models.fields.NOT_PROVIDED,
            'field_type': models.TextField,
            'null': True,
            'unique': False,
        },
        'created': {
            'blank': False,
            'default': models.fields.NOT_PROVIDED,
            'field_type': models.DateTimeField,
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



class TenantModelInheritedCases(
    TenantModelTestCases,
):
    pass



class TenantModelPyTest(
    TenantModelTestCases,
):
    pass

import pytest

from django.db import models

from core.tests.unit.centurion_abstract.test_unit_centurion_abstract_model import (
    CenturionAbstractTenancyModelInheritedCases
)



@pytest.mark.model_featureflag
class FeatureFlagModelTestCases(
    CenturionAbstractTenancyModelInheritedCases
):


    @property
    def parameterized_class_attributes(self):

        return {
            'model_tag': {
                'type': str,
                'value': 'feature_flag'
            },
        }


    @property
    def parameterized_model_fields(self):
        
        return {
        'software': {
            'blank': False,
            'default': models.fields.NOT_PROVIDED,
            'field_type': models.ForeignKey,
            'null': False,
            'unique': False,
        },
        'name': {
            'blank': False,
            'default': models.fields.NOT_PROVIDED,
            'field_type': models.CharField,
            'length': 50,
            'null': False,
            'unique': False,
        },
        'description': {
            'blank': True,
            'default': models.fields.NOT_PROVIDED,
            'field_type': models.TextField,
            'null': True,
            'unique': False,
        },
        'enabled': {
            'blank': False,
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



class FeatureFlagModelInheritedCases(
    FeatureFlagModelTestCases,
):
    pass



@pytest.mark.module_devops
class FeatureFlagModelPyTest(
    FeatureFlagModelTestCases,
):
    pass

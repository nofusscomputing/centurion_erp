import pytest

from django.db import models


from core.tests.unit.centurion_abstract.test_unit_centurion_abstract_model import (
    CenturionAbstractTenancyModelInheritedCases
)



@pytest.mark.model_externallink
class AppSettingsModelTestCases(
    CenturionAbstractTenancyModelInheritedCases
):


    @property
    def parameterized_class_attributes(self):

        return {
            'model_tag': {
                'value': 'external_link'
            },
        }


    @property
    def parameterized_model_fields(self):

        return {
            'name': {
                'blank': False,
                'default': models.fields.NOT_PROVIDED,
                'field_type': models.CharField,
                'length': 30,
                'null': False,
                'unique': True,
            },
            'button_text': {
                'blank': True,
                'default': models.fields.NOT_PROVIDED,
                'field_type': models.CharField,
                'length': 30,
                'null': True,
                'unique': True,
            },
            'template': {
                'blank': False,
                'default': models.fields.NOT_PROVIDED,
                'field_type': models.CharField,
                'length': 180,
                'null': False,
                'unique': False,
            },
            'colour': {
                'blank': True,
                'default': models.fields.NOT_PROVIDED,
                'field_type': models.CharField,
                'length': 180,
                'null': True,
                'unique': False,
            },
            'cluster': {
                'blank': False,
                'default': False,
                'field_type': models.BooleanField,
                'null': False,
                'unique': False,
            },
            'devices': {
                'blank': False,
                'default': False,
                'field_type': models.BooleanField,
                'null': False,
                'unique': False,
            },
            'service': {
                'blank': False,
                'default': False,
                'field_type': models.BooleanField,
                'null': False,
                'unique': False,
            },
            'software': {
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



class AppSettingsModelInheritedCases(
    AppSettingsModelTestCases,
):
    pass



@pytest.mark.module_settings
class AppSettingsModelPyTest(
    AppSettingsModelTestCases,
):

    pass

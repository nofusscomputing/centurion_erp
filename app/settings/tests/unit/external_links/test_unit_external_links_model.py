import pytest

from django.db import models


from core.tests.unit.centurion_abstract.test_unit_centurion_abstract_model import (
    CenturionAbstractModelInheritedCases
)



@pytest.mark.model_externallink
class AppSettingsModelTestCases(
    CenturionAbstractModelInheritedCases
):


    @property
    def parameterized_class_attributes(self):

        return {
            'model_tag': {
                'type': models.fields.NOT_PROVIDED,
                'value': models.fields.NOT_PROVIDED
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

        def test_model_tag_defined(self, model):
            """ Model Tag

            Ensure that the model has a tag defined.
            """

            pytest.xfail( reason = 'Model does not require tag' )

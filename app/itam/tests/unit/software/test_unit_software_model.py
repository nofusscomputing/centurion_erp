import pytest

from django.db import models


from core.tests.unit.centurion_abstract.test_unit_centurion_abstract_model import (
    CenturionAbstractTenancyModelInheritedCases
)



@pytest.mark.model_software
class SoftwareModelTestCases(
    CenturionAbstractTenancyModelInheritedCases
):


    @property
    def parameterized_class_attributes(self):

        return {
            'model_tag': {
                'value': 'software'
            },
        }


    @property
    def parameterized_model_fields(self):

        return {
            'publisher': {
                'blank': True,
                'default': models.fields.NOT_PROVIDED,
                'field_type': models.ForeignKey,
                'null': True,
                'unique': False,
            },
            'name': {
                'blank': False,
                'default': models.fields.NOT_PROVIDED,
                'field_type': models.CharField,
                'length': 50,
                'null': False,
                'unique': True,
            },
            'category': {
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



class SoftwareModelInheritedCases(
    SoftwareModelTestCases,
):
    pass



@pytest.mark.module_itam
class SoftwareModelPyTest(
    SoftwareModelTestCases,
):
    pass

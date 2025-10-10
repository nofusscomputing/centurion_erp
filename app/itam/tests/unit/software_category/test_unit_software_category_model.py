import pytest

from django.db import models


from core.tests.unit.centurion_abstract.test_unit_centurion_abstract_model import (
    CenturionAbstractTenancyModelInheritedCases
)



@pytest.mark.model_softwarecategory
class SoftwareCategoryModelTestCases(
    CenturionAbstractTenancyModelInheritedCases
):


    @property
    def parameterized_class_attributes(self):

        return {
            'model_tag': {
                'value': 'software_category'
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



class SoftwareCategoryModelInheritedCases(
    SoftwareCategoryModelTestCases,
):
    pass



@pytest.mark.module_itam
class SoftwareCategoryModelPyTest(
    SoftwareCategoryModelTestCases,
):
    pass

import pytest

from django.db import models


from core.tests.unit.centurion_abstract.test_unit_centurion_abstract_model import (
    CenturionAbstractTenancyModelInheritedCases
)



@pytest.mark.model_projecttype
class ProjectTypeModelTestCases(
    CenturionAbstractTenancyModelInheritedCases
):


    @property
    def parameterized_class_attributes(self):

        return {
            'model_tag': {
                'type': str,
                'value': 'project_type'
            },
        }


    @property
    def parameterized_model_fields(self):

        return {
            'name': {
                'blank': False,
                'default': models.fields.NOT_PROVIDED,
                'field_type': models.CharField,
                'length': 100,
                'null': False,
                'unique': True,
            },
            'runbook': {
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



class ProjectTypeModelInheritedCases(
    ProjectTypeModelTestCases,
):
    pass



@pytest.mark.module_project_management
class ProjectTypeModelPyTest(
    ProjectTypeModelTestCases,
):

    pass
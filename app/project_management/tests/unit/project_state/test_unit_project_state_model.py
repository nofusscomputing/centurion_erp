import pytest

from django.db import models


from core.tests.unit.centurion_abstract.test_unit_centurion_abstract_model import (
    CenturionAbstractTenancyModelInheritedCases
)



@pytest.mark.model_projectstate
class ProjectStateModelTestCases(
    CenturionAbstractTenancyModelInheritedCases
):


    @property
    def parameterized_class_attributes(self):

        return {
            'model_tag': {
                'type': str,
                'value': 'project_state'
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
            'is_completed': {
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



class ProjectStateModelInheritedCases(
    ProjectStateModelTestCases,
):
    pass



@pytest.mark.module_project_management
class ProjectStateModelPyTest(
    ProjectStateModelTestCases,
):

    pass
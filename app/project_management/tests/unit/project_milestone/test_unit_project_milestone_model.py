import pytest

from django.db import models


from core.tests.unit.centurion_abstract.test_unit_centurion_abstract_model import (
    CenturionAbstractModelInheritedCases
)



@pytest.mark.model_projectmilestone
class ProjectMilestoneModelTestCases(
    CenturionAbstractModelInheritedCases
):


    @property
    def parameterized_class_attributes(self):

        return {
            '_ticket_linkable': {
                'value': False,
            },
            'model_tag': {
                'type': str,
                'value': 'project_milestone'
            },
        }


    @property
    def parameterized_model_fields(self):

        return {
            'model_notes': {
                'blank': models.fields.NOT_PROVIDED,
                'default': models.fields.NOT_PROVIDED,
                'field_type': models.fields.NOT_PROVIDED,
                'null': models.fields.NOT_PROVIDED,
                'unique': models.fields.NOT_PROVIDED,
            },
            'name': {
                'blank': False,
                'default': models.fields.NOT_PROVIDED,
                'field_type': models.CharField,
                'length': 100,
                'null': False,
                'unique': True,
            },
            'description': {
                'blank': True,
                'default': models.fields.NOT_PROVIDED,
                'field_type': models.TextField,
                'null': True,
                'unique': False,
            },
            'start_date': {
                'blank': True,
                'default': models.fields.NOT_PROVIDED,
                'field_type': models.DateTimeField,
                'null': True,
                'unique': False,
            },
            'finish_date': {
                'blank': True,
                'default': models.fields.NOT_PROVIDED,
                'field_type': models.DateTimeField,
                'null': True,
                'unique': False,
            },
            'project': {
                'blank': False,
                'default': models.fields.NOT_PROVIDED,
                'field_type': models.ForeignKey,
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



class ProjectMilestoneModelInheritedCases(
    ProjectMilestoneModelTestCases,
):
    pass



@pytest.mark.module_project_management
class ProjectMilestoneModelPyTest(
    ProjectMilestoneModelTestCases,
):


    def test_method_get_url_kwargs(self, mocker, model_instance, model_kwargs):
        """Test Class Method
        
        Ensure method `get_url_kwargs` returns the correct value.
        """


        url = model_instance.get_url_kwargs()

        assert model_instance.get_url_kwargs() == {
            'project_id': model_kwargs['project'].id,
            'pk': model_instance.id
        }


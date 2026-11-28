from django.core.exceptions import ValidationError
import pytest

from django.db import models


from core.tests.unit.centurion_abstract.test_unit_centurion_abstract_model import (
    CenturionAbstractTenancyModelInheritedCases
)

from project_management.models.projects import Project



@pytest.mark.model_project
class ClusterModelTestCases(
    CenturionAbstractTenancyModelInheritedCases
):


    @property
    def parameterized_class_attributes(self):

        return {
            '_ticket_linkable': {
                'value': False,
            },
            'model_tag': {
                'type': str,
                'value': 'project'
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
        'external_ref': {
            'blank': True,
            'default': models.fields.NOT_PROVIDED,
            'field_type': models.IntegerField,
            'null': True,
            'unique': False,
        },
        'external_system': {
            'blank': True,
            'default': models.fields.NOT_PROVIDED,
            'field_type': models.IntegerField,
            'null': True,
            'unique': False,
        },
        "parent": {
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
        'priority': {
            'blank': False,
            'default': Project.Priority.LOW,
            'field_type': models.IntegerField,
            'null': True,
            'unique': False,
        },
        'state': {
            'blank': True,
            'default': models.fields.NOT_PROVIDED,
            'field_type': models.ForeignKey,
            'null': True,
            'unique': False,
        },
        'project_type': {
            'blank': True,
            'default': models.fields.NOT_PROVIDED,
            'field_type': models.ForeignKey,
            'null': True,
            'unique': False,
        },
        'code': {
            'blank': True,
            'default': models.fields.NOT_PROVIDED,
            'field_type': models.CharField,
            'length': 25,
            'null': True,
            'unique': True,
        },
        'planned_start_date': {
            'blank': True,
            'default': models.fields.NOT_PROVIDED,
            'field_type': models.DateTimeField,
            'null': True,
            'unique': False,
        },
        'planned_finish_date': {
            'blank': True,
            'default': models.fields.NOT_PROVIDED,
            'field_type': models.DateTimeField,
            'null': True,
            'unique': False,
        },
        'real_start_date': {
            'blank': True,
            'default': models.fields.NOT_PROVIDED,
            'field_type': models.DateTimeField,
            'null': True,
            'unique': False,
        },
        'real_finish_date': {
            'blank': True,
            'default': models.fields.NOT_PROVIDED,
            'field_type': models.DateTimeField,
            'null': True,
            'unique': False,
        },
        'manager_user': {
            'blank': True,
            'default': models.fields.NOT_PROVIDED,
            'field_type': models.ForeignKey,
            'null': True,
            'unique': False,
        },
        'manager_team': {
            'blank': True,
            'default': models.fields.NOT_PROVIDED,
            'field_type': models.ForeignKey,
            'null': True,
            'unique': False,
        },
        'team_members': {
            'blank': True,
            'default': models.fields.NOT_PROVIDED,
            'field_type': models.ManyToManyField,
            'null': False,
            'unique': False,
        },
        'is_deleted': {
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



    def test_field_parent_cant_set_self(self,
        model, model_kwargs
    ):
        """ Field Check

        Ensure that the parent project cant be set to self.
        """


        parent_kwargs = model_kwargs()
        del parent_kwargs['team_members']

        parent_obj = model( **parent_kwargs )

        kwargs = model_kwargs()
        del kwargs['team_members']
        kwargs ['parent'] = parent_obj

        obj = model( **kwargs )

        obj.id = 98765432
        obj.pk = obj.id

        obj.parent.id = obj.pk
        obj.parent.pk = obj.pk

        with pytest.raises( ValidationError ) as exc:

            obj.clean_fields()

        assert exc.value.args[1] == 'self_not_parent'



class ClusterModelInheritedCases(
    ClusterModelTestCases,
):
    pass



@pytest.mark.module_project_management
class ClusterModelPyTest(
    ClusterModelTestCases,
):
    pass

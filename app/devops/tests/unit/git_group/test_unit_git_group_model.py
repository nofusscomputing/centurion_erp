import pytest

from django.db import models


from core.tests.unit.centurion_abstract.test_unit_centurion_abstract_model import (
    CenturionAbstractModelInheritedCases
)

from devops.models.git_group import GitGroup



@pytest.mark.model_gitgroup
class GitGroupModelTestCases(
    CenturionAbstractModelInheritedCases
):



    kwargs_create_item = {
            'parent_group': None,
            'provider': GitGroup.GitProvider.GITHUB,
            'provider_pk': 1,
            'name': 'a name',
            'path': 'a_path',
            'description': 'a random bit of text.'
        }



    @property
    def parameterized_class_attributes(self):
        
        return {
            'is_global': {
                'type': type(None),
                'value': None,
            },
        }


    parameterized_model_fields = {
        'parent_group': {
            'blank': True,
            'default': models.fields.NOT_PROVIDED,
            'field_type': models.ForeignKey,
            'null': True,
            'unique': False,
        },
        'provider': {
            'blank': False,
            'default': models.fields.NOT_PROVIDED,
            'field_type': models.IntegerField,
            'null': False,
            'unique': False,
        },
        'provider_pk': {
            'blank': True,
            'default': models.fields.NOT_PROVIDED,
            'field_type': models.IntegerField,
            'null': True,
            'unique': False,
        },
        'name': {
            'blank': False,
            'default': models.fields.NOT_PROVIDED,
            'field_type': models.IntegerField,
            'length': 80,
            'null': False,
            'unique': False,
        },
        'path': {
            'blank': False,
            'default': models.fields.NOT_PROVIDED,
            'field_type': models.IntegerField,
            'length': 80,
            'null': False,
            'unique': False,
        },
        'description': {
            'blank': True,
            'default': models.fields.NOT_PROVIDED,
            'field_type': models.IntegerField,
            'max_length': 80,
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



class GitGroupModelInheritedCases(
    GitGroupModelTestCases,
):
    pass



class GitGroupModelPyTest(
    GitGroupModelTestCases,
):
    pass

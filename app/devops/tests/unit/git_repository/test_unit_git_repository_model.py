import pytest

from django.db import models

from core.tests.unit.centurion_abstract.test_unit_centurion_abstract_model import (
    CenturionAbstractModelInheritedCases
)

from devops.models.git_group import GitGroup


@pytest.mark.model_gitrepository
class GitRepositoryBaseModelTestCases(
    CenturionAbstractModelInheritedCases
):


    @property
    def parameterized_class_attributes(self):

        return {
            'model_tag': {
                'type': str,
                'value': 'git_repository'
            },
            'url_model_name': {
                'type': str,
                'value': 'gitrepository'
            },
        }


    parameterized_model_fields = {
        'provider': {
            'blank': False,
            'default': models.fields.NOT_PROVIDED,
            'field_type': models.IntegerField,
            'null': False,
            'unique': False,
        },
        'provider_id': {
            'blank': True,
            'default': models.fields.NOT_PROVIDED,
            'field_type': models.IntegerField,
            'null': True,
            'unique': False,
        },
        'git_group': {
            'blank': False,
            'default': models.fields.NOT_PROVIDED,
            'field_type': models.ForeignKey,
            'null': False,
            'unique': False,
        },
        'path': {
            'blank': False,
            'default': models.fields.NOT_PROVIDED,
            'field_type': models.CharField,
            'length': 80,
            'null': False,
            'unique': False,
        },
        'name': {
            'blank': False,
            'default': models.fields.NOT_PROVIDED,
            'field_type': models.CharField,
            'length': 80,
            'null': False,
            'unique': False,
        },
        'description': {
            'blank': True,
            'default': models.fields.NOT_PROVIDED,
            'field_type': models.TextField,
            'length': 300,
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


    def test_method_get_url_kwargs(self, mocker, model_instance, settings):
        """Test Class Method
        
        Ensure method `get_url_kwargs` returns the correct value.
        """

        if model_instance.provider == GitGroup.GitProvider.GITHUB:

            provider = 'github'

        elif model_instance.provider == GitGroup.GitProvider.GITLAB:

            provider = 'gitlab'


        url = model_instance.get_url_kwargs()

        assert model_instance.get_url_kwargs() == {
            # 'git_provider': provider,
            'pk': model_instance.id
        }


class GitRepositoryBaseModelInheritedCases(
    GitRepositoryBaseModelTestCases,
):

    pass



@pytest.mark.module_devops
class GitRepositoryBaseModelPyTest(
    GitRepositoryBaseModelTestCases,
):
    pass

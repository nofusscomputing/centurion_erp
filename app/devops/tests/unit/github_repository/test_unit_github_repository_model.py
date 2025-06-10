import pytest

from django.db import models

from core.tests.unit.centurion_sub_abstract.test_unit_centurion_sub_abstract_model import (
    CenturionSubAbstractModelInheritedCases
)

from devops.tests.unit.git_repository.test_unit_git_repository_model import (
    GitRepositoryBaseModelInheritedCases
)



@pytest.mark.model_githubrepository
class GitHubRepositoryBaseModelTestCases(
    CenturionSubAbstractModelInheritedCases,
    GitRepositoryBaseModelInheritedCases,
):


    # @property
    # def parameterized_class_attributes(self):

    #     return {
    #         'is_sub': {
    #             'type': str,
    #             'value': 'git_repository'
    #         },
    #     }

    @property
    def parameterized_model_fields(self):
        
        return {
        'wiki': {
            'blank': False,
            'default': False,
            'field_type': models.BooleanField,
            'null': False,
            'unique': False,
        },
        'issues': {
            'blank': False,
            'default': False,
            'field_type': models.BooleanField,
            'null': False,
            'unique': False,
        },
        'sponsorships': {
            'blank': False,
            'default': False,
            'field_type': models.BooleanField,
            'null': False,
            'unique': False,
        },
        'preserve_this_repository': {
            'blank': False,
            'default': False,
            'field_type': models.BooleanField,
            'null': False,
            'unique': False,
        },
        'discussions': {
            'blank': False,
            'default': False,
            'field_type': models.BooleanField,
            'null': False,
            'unique': False,
        },
        'projects': {
            'blank': False,
            'default': False,
            'field_type': models.BooleanField,
            'null': False,
            'unique': False,
        }
    }



class GitHubRepositoryBaseModelInheritedCases(
    GitHubRepositoryBaseModelTestCases,
):

    pass



@pytest.mark.module_devops
class GitHubRepositoryBaseModelPyTest(
    GitHubRepositoryBaseModelTestCases,
):
    pass

import pytest

from django.db import models

from core.tests.unit.centurion_sub_abstract.test_unit_centurion_sub_abstract_model import (
    CenturionSubAbstractModelInheritedCases
)

from devops.tests.unit.git_repository.test_unit_git_repository_model import (
    GitRepositoryBaseModelInheritedCases
)



@pytest.mark.model_gitlabrepository
class GitLabRepositoryBaseModelTestCases(
    CenturionSubAbstractModelInheritedCases,
    GitRepositoryBaseModelInheritedCases,
):

    parameterized_model_fields = {
        'visibility': {
            'blank': False,
            'default': models.NOT_PROVIDED,
            'field_type': models.BooleanField,
            'null': False,
            'unique': False,
        }
    }



class GitLabRepositoryBaseModelInheritedCases(
    GitLabRepositoryBaseModelTestCases,
):

    pass



@pytest.mark.module_devops
class GitLabRepositoryBaseModelPyTest(
    GitLabRepositoryBaseModelTestCases,
):
    pass

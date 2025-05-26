import pytest

from core.tests.functional.centurion_abstract.test_functional_centurion_abstract_model import (
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



class GitGroupModelInheritedCases(
    GitGroupModelTestCases,
):
    pass



class GitGroupModelPyTest(
    GitGroupModelTestCases,
):
    pass

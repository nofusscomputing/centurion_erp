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



    def test_model_create_with_parent_sets_tenancy(self, created_model, model):
        """Model Created

        Ensure that the model when created with a parent git group, that its
        tenancy is set to that of the parent group
        """

        kwargs_create_item = self.kwargs_create_item.copy()

        del kwargs_create_item['organization']
        kwargs_create_item['parent_group'] = created_model

        child_group = model.objects.create(
            **kwargs_create_item
        )

        organization = child_group.organization

        child_group.delete()

        assert child_group.organization == created_model.organization



class GitGroupModelInheritedCases(
    GitGroupModelTestCases,
):
    pass



class GitGroupModelPyTest(
    GitGroupModelTestCases,
):
    pass

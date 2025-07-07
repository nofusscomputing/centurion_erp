import pytest

from django.core.exceptions import (
    ValidationError
)

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


    @pytest.mark.skip( reason = 'test must be as part of serializer and viewset tests, not model' )
    def test_model_create_has_history_entry(self, model_contenttype, created_model, model):
        """Model Created

        Ensure that the model when created, added a `create` Audit History
        entry.
        """

        pass


    def test_model_create_with_parent_sets_tenancy(self, created_model, model):
        """Model Created

        Ensure that the model when created with a parent git group, that its
        tenancy is set to that of the parent group
        """

        kwargs_create_item = self.kwargs_create_item.copy()

        kwargs_create_item['provider'] = model.GitProvider.GITLAB

        del kwargs_create_item['organization']
        kwargs_create_item['parent_group'] = created_model

        child_group = model.objects.create(
            **kwargs_create_item
        )

        organization = child_group.organization

        child_group.delete()

        assert child_group.organization == created_model.organization



    def test_model_create_with_parent_exception_github(self, created_model, model):
        """Model Created

        Ensure that the model when created with a parent git group, with the
        provider being Github, that an exception is thrown as Github groups
        can't have parents/nesting.
        """

        kwargs_create_item = self.kwargs_create_item.copy()

        kwargs_create_item['provider'] = model.GitProvider.GITHUB

        del kwargs_create_item['organization']
        kwargs_create_item['parent_group'] = created_model

        with pytest.raises( ValidationError ) as e:

            child_group = model.objects.create(
                **kwargs_create_item
            )

            child_group.delete()

        assert e.value.error_dict['__all__'][0].code == 'no_parent_for_github_group'



class GitGroupModelInheritedCases(
    GitGroupModelTestCases,
):
    pass



class GitGroupModelPyTest(
    GitGroupModelTestCases,
):
    pass

import pytest

from django.core.exceptions import (
    ValidationError
)

from core.tests.functional.centurion_abstract.test_functional_centurion_abstract_model import (
    CenturionAbstractTenancyModelInheritedCases
)



@pytest.mark.model_gitgroup
class GitGroupModelTestCases(
    CenturionAbstractTenancyModelInheritedCases
):


    def test_model_create_with_parent_sets_tenancy(self, created_model, model, model_kwargs):
        """Model Created

        Ensure that the model when created with a parent git group, that its
        tenancy is set to that of the parent group
        """

        kwargs = model_kwargs()

        kwargs['provider'] = model.GitProvider.GITLAB

        del kwargs['organization']
        kwargs['parent_group'] = created_model

        child_group = model.objects.create(
            **kwargs
        )

        organization = child_group.organization

        child_group.delete()

        assert child_group.organization == created_model.organization



    def test_model_create_with_parent_exception_github(self, created_model, model, model_kwargs):
        """Model Created

        Ensure that the model when created with a parent git group, with the
        provider being Github, that an exception is thrown as Github groups
        can't have parents/nesting.
        """

        kwargs = model_kwargs()

        kwargs['provider'] = model.GitProvider.GITHUB

        del kwargs['organization']
        kwargs['parent_group'] = created_model

        with pytest.raises( ValidationError ) as e:

            child_group = model.objects.create(
                **kwargs
            )

            child_group.delete()

        assert e.value.error_dict['__all__'][0].code == 'no_parent_for_github_group'


class GitGroupModelInheritedCases(
    GitGroupModelTestCases,
):
    pass



@pytest.mark.module_access
class GitGroupModelPyTest(
    GitGroupModelTestCases,
):
    pass

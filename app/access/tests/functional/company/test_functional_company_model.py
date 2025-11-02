import pytest

from django.core.exceptions import ValidationError

from access.tests.functional.entity.test_functional_entity_model import EntityModelInheritedCases

from settings.models.app_settings import (
    AppSettings
)



@pytest.mark.model_company
class CompanyModelTestCases(
    EntityModelInheritedCases
):


    def test_function_create_global_company_set_manufacturer_is_global_set(self,
        model, model_kwargs,
        organization_two
    ):
        """Test function Create
        
        If global manufacturer is set, ensure when creating model that the
        organization is set to the global organization.
        """
        
        settings = AppSettings.objects.get( owner_organization = None )

        settings.global_organization = organization_two

        settings.manufacturer_is_global = True

        settings.save()

        assert settings.global_organization == organization_two, 'Global organization must be set for test to progress.'

        kwargs = model_kwargs()

        obj = model.objects.create( **kwargs )


        assert obj.organization == organization_two


    def test_function_create_global_company_not_set_manufacturer_is_global_set(self,
        model, model_kwargs,
        organization_two
    ):
        """Test function Create
        
        If global manufacturer is set, ensure when creating model that the
        organization is set to the global organization.
        """
        
        settings = AppSettings.objects.get( owner_organization = None )

        settings.global_organization = None

        settings.manufacturer_is_global = True

        settings.save()

        assert settings.global_organization == None, 'Global organization must be set for test to progress.'

        kwargs = model_kwargs()

        with pytest.raises(ValidationError) as exc:
            obj = model.objects.create( **kwargs )


        assert exc.value.error_dict['organization'][0].code == 'no_global_org_set'


    def test_function_create_global_company_set_manufacturer_is_global_not_set(self,
        model, model_kwargs,
        organization_two
    ):
        """Test function Create
        
        If global manufacturer is set, ensure when creating model that the
        organization is set to the global organization.
        """
        
        settings = AppSettings.objects.get( owner_organization = None )

        settings.global_organization = organization_two

        settings.manufacturer_is_global = False

        settings.save()

        assert settings.global_organization == organization_two, 'Global organization must be set for test to progress.'

        kwargs = model_kwargs()

        obj = model.objects.create( **kwargs )


        assert obj.organization == kwargs['organization']


    def test_function_create_global_company_not_set_manufacturer_is_global_not_set(self,
        model, model_kwargs,
        organization_two
    ):
        """Test function Create
        
        If global manufacturer is set, ensure when creating model that the
        organization is set to the global organization.
        """
        
        settings = AppSettings.objects.get( owner_organization = None )

        settings.global_organization = None

        settings.manufacturer_is_global = False

        settings.save()

        assert settings.global_organization == None, 'Global organization must be set for test to progress.'

        kwargs = model_kwargs()

        obj = model.objects.create( **kwargs )


        assert obj.organization == kwargs['organization']



class CompanyModelInheritedCases(
    CompanyModelTestCases,
):
    pass


@pytest.mark.module_access
class CompanyModelPyTest(
    CompanyModelTestCases,
):
    pass

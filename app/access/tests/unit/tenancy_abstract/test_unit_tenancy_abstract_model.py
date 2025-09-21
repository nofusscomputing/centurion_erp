import pytest

from django.db import models

from access.models.tenancy_abstract import TenancyAbstractModel
from access.tests.unit.managers.test_unit_tenancy_manager import (
    TenancyManagerInheritedCases
)

from centurion.tests.unit_models import ModelTestCases


@pytest.mark.unit
@pytest.mark.tenancy_models
class TenancyAbstractModelTestCases(
    TenancyManagerInheritedCases,
    ModelTestCases,
):


    @property
    def parameterized_class_attributes(self):

        return {}


    @property
    def parameterized_model_fields(self):

        return {
        'organization': {
            'blank': False,
            'default': models.fields.NOT_PROVIDED,
            'field_type': models.ForeignKey,
            'null': False,
            'unique': False,
        },
    }


    @pytest.fixture( scope = 'class', autouse = True)
    def setup_organization(cls, request, model, organization_one, model_kwargs):

        request.cls.organization = organization_one

        if request.cls.kwargs_create_item:

            request.cls.kwargs_create_item.update({
                'organization': organization_one,
            })

        else:

            request.cls.kwargs_create_item = {
                'organization': organization_one,
            }



    def test_class_inherits_tenancy_model(self, model):
        """ Class Check

        Ensure this model inherits from `TenancyAbstractModel`
        """

        assert issubclass(model, TenancyAbstractModel)



    def test_method_get_tenant_returns_tenant(self, mocker, model_instance):
        """Test Class Method
        
        Ensure method `get_history_model_name` returns the value of the models
        audit name `<Model Class name>AuditHistory`
        """

        test_value = self.organization
        model_instance.organization = test_value


        assert model_instance.get_tenant() == test_value

    def test_method_clean_fields_calls_super_tenancy_abstract(self, mocker, model_instance):
        """Test Class Method

        Ensure method `clean_fields` calls `super().clean_fields`
        """

        super_clean_fields = mocker.patch(
            'django.db.models.base.Model.clean_fields', return_value = None
        )

        model_instance.clean_fields()

        super_clean_fields.assert_called_once()


    def test_method_clean_calls_super_tenancy_abstract(self, mocker, model_instance):
        """Test Class Method

        Ensure method `clean` calls `super().clean`
        """

        super_clean = mocker.patch('django.db.models.base.Model.clean', return_value = None)

        model_instance.clean()


        super_clean.assert_called_once()


    def test_method_validate_constraints_calls_super_tenancy_abstract(self, mocker, model_instance):
        """Test Class Method

        Ensure method `validate_constraints` calls `super().validate_constraints`
        """

        super_validate_constraints = mocker.patch(
            'django.db.models.base.Model.validate_constraints', return_value = None
        )

        model_instance.validate_constraints()


        super_validate_constraints.assert_called_once()


    def test_method_validate_unique_calls_super_tenancy_abstract(self, mocker, model_instance):
        """Test Class Method

        Ensure method `validate_unique` calls `super().validate_unique`
        """

        super_validate_unique = mocker.patch(
            'django.db.models.base.Model.validate_unique', return_value = None
        )

        model_instance.validate_unique()

        super_validate_unique.assert_called_once()


    def test_method_full_clean_calls_super_tenancy_abstract(self, mocker, model_instance):
        """Test Class Method

        Ensure method `full_clean` calls `super().full_clean`
        """

        super_validate_unique = mocker.patch(
            'django.db.models.base.Model.full_clean', return_value = None
        )

        model_instance.full_clean()

        super_validate_unique.assert_called_once()



class TenancyAbstractModelInheritedCases(
    TenancyAbstractModelTestCases,
):


    pass



@pytest.mark.module_access
class TenancyAbstractModelPyTest(
    TenancyAbstractModelTestCases,
):


    def test_model_is_abstract(self, model):

        assert model._meta.abstract



    def test_method_get_tenant_returns_tenant(self, mocker, model_instance):
        """Test Class Method
        
        Ensure method `get_history_model_name` returns the value of the models
        audit name `<Model Class name>AuditHistory`
        """

        test_value = self.organization
        model_instance.organization = test_value


        assert model_instance.get_tenant() == test_value

    def test_manager_tenancy_filter_tenant(self):
        pytest.xfail( reason = 'base model, test is n/a.' )

    def test_manager_tenancy_select_related(self):
        pytest.xfail( reason = 'base model, test is n/a.' )

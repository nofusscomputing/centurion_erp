import inspect
import pytest

from django.db import models

from centurion.tests.unit_models import ModelTestCases

from access.models.tenancy_abstract import TenancyAbstractModel



@pytest.mark.tenancy_models
class TenancyAbstractModelTestCases(
    ModelTestCases
):


    parameterized_class_attributes = {
        'context': {
            'type': dict,
            # 'value': {
            #     'logger': None,
            #     'user': None,
            # }
        }
    }


    parameterized_model_fields = {
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



class TenancyAbstractModelInheritedCases(
    TenancyAbstractModelTestCases,
):


    pass



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


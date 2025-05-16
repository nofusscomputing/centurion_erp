import pytest

from django.db import models

from accounting.models.asset_base import AssetBase

from centurion.tests.unit.test_unit_models import (
    PyTestTenancyObjectInheritedCases,
)



class AssetBaseModelTestCases(
    PyTestTenancyObjectInheritedCases,
):

    base_model = AssetBase

    kwargs_create_item: dict = {
        'asset_number': 'a12s432',
        'serial_number': 'abbcccdddd',
    }

    sub_model_type = 'asset'
    """Sub Model Type
    
    sub-models must have this attribute defined in `ModelName.Meta.sub_model_type`
    """


    parameterized_fields: dict = {
        "is_global": {
            'field_type': None,
            'field_parameter_default_exists': None,
            'field_parameter_default_value': None,
            'field_parameter_verbose_name_type': None
        },
        "asset_number": {
            'field_type': models.fields.CharField,
            'field_parameter_default_exists': False,
            'field_parameter_verbose_name_type': str,
        },
        "serial_number": {
            'field_type': models.fields.CharField,
            'field_parameter_default_exists': False,
            'field_parameter_verbose_name_type': str,
        }
        
    }



    @pytest.fixture( scope = 'class')
    def setup_model(self,
        request,
        model,
        django_db_blocker,
        organization_one,
        organization_two
    ):

        with django_db_blocker.unblock():

            request.cls.organization = organization_one

            request.cls.different_organization = organization_two

            kwargs_create_item = {}

            for base in reversed(request.cls.__mro__):

                if hasattr(base, 'kwargs_create_item'):

                    if base.kwargs_create_item is None:

                        continue

                    kwargs_create_item.update(**base.kwargs_create_item)


            if len(kwargs_create_item) > 0:

                request.cls.kwargs_create_item = kwargs_create_item


            if 'organization' not in request.cls.kwargs_create_item:

                request.cls.kwargs_create_item.update({
                    'organization': request.cls.organization
                })

        yield

        with django_db_blocker.unblock():

            del request.cls.kwargs_create_item


    @pytest.fixture( scope = 'class', autouse = True)
    def class_setup(self,
        setup_model,
        create_model,
    ):

        pass



    def test_class_inherits_assetbase(self):
        """ Class inheritence

        TenancyObject must inherit SaveHistory
        """

        assert issubclass(self.model, AssetBase)



    def test_attribute_type_app_namespace(self):
        """Attribute Type

        app_namespace is of type str
        """

        assert type(self.model.app_namespace) is str


    def test_attribute_value_app_namespace(self):
        """Attribute Type

        app_namespace has been set, override this test case with the value
        of attribute `app_namespace`
        """

        assert self.model.app_namespace == 'accounting'


    def test_function_is_property_get_model_type(self):
        """Function test

        Confirm function `get_model_type` is a property
        """

        assert type(self.model.get_model_type) is property


    def test_function_value_get_model_type(self):
        """Function test

        Confirm function `get_model_type` returns None for base model
        """

        assert self.item.get_model_type is None


    def test_function_value_get_related_model(self):
        """Function test

        Confirm function `get_related_model` is of the sub-model type
        """

        assert type(self.item.get_related_model()) == self.model


    def test_function_value_get_url(self):

        assert self.item.get_url() == '/api/v2/accounting/asset/' + str(self.item.id)



class AssetBaseModelInheritedCases(
    AssetBaseModelTestCases,
):
    """Sub-Ticket Test Cases

    Test Cases for Ticket models that inherit from model AssetBase
    """

    kwargs_create_item: dict = {}

    model = None


    sub_model_type = None
    """Ticket Sub Model Type
    
    Ticket sub-models must have this attribute defined in `ModelNam.Meta.sub_model_type`
    """


    def test_function_value_get_model_type(self):
        """Function test

        Confirm function `get_model_type` does not have a value of None
        value should be equaul to Meta.sub_model_type
        """

        assert self.item.get_model_type == self.item._meta.sub_model_type



class AssetBaseModelPyTest(
    AssetBaseModelTestCases,
):


    def test_function_value_get_related_model(self):
        """Function test

        Confirm function `get_related_model` is None for base model
        """

        assert self.item.get_related_model() is None

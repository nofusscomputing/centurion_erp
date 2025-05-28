import pytest

from django.apps import apps
from django.db import models

from centurion.tests.unit_class import ClassTestCases


@pytest.mark.models
@pytest.mark.unit
class ModelTestCases(
    ClassTestCases
):
    """Model Common Test Suite

    This test suite contains all of the common tests for **ALL** Centurion
    Models.

    ## Fields

    To test the fields define class attribute or a property called
    `parameterized_model_fields` that is a dict. i.e

    ``` py

    parameterized_model_fields = {
        '<model field name>': {
            'blank': ,
            'default': ,
            'field_type': ,
            'null': ,
            'unique': ,
        }
    }

    ```

    This fields tests the following attributes, which must be specified. If the
    field is not defined with an attribute, add the default value:

    - Fields:

        - Type the model field is

        - Value of Parameter `blank`

        - Value of Parameter `default`

        - Value of Parameter `null`

        - Value of Parameter `unique`

    Default values for field attributes are:
        
    ``` py
    {
        'blank': True,
        'default': models.fields.NOT_PROVIDED,
        'null': False,
        'unique': False,
    }

    ```

    """

    @pytest.fixture( scope = 'class')
    def test_class(cls, model):

        yield model


    @pytest.fixture( scope = 'function', autouse = True)
    def model_instance(cls, request, model):

        if model._meta.abstract:

            class MockModel(model):
                class Meta:
                    app_label = 'core'
                    verbose_name = 'mock instance'
                    managed = False

            instance = MockModel()

        else:

            instance = model()

        yield instance

        del instance

        if 'mockmodel' in apps.all_models['core']:

            del apps.all_models['core']['mockmodel']



    @pytest.fixture( scope = 'class', autouse = True)
    def setup_class(cls, request, model):
        
        pass



    @property
    def parameterized_model_fields(self):
        return {}



    def test_model_field_parameter_value_blank(self,
        model_instance, 
        parameterized, param_key_model_fields, param_field_name, param_blank
    ):
        """Test Model Field Parameter

        Ensure field parameter `param_field_name` has a value of `param_blank`
        """

        if param_blank == models.fields.NOT_PROVIDED:

            assert True

        else:

            assert getattr(model_instance._meta.get_field(param_field_name), 'blank') == param_blank



    def test_model_field_parameter_value_default(self,
        model_instance, 
        parameterized, param_key_model_fields, param_field_name, param_default
    ):
        """Test Model Field Parameter

        Ensure field parameter `param_field_name` has a value of `param_default`
        """


        if param_default == models.fields.NOT_PROVIDED:

            assert True

        else:

            assert getattr(model_instance._meta.get_field(param_field_name), 'default') == param_default



    def test_model_field_parameter_value_null(self,
        model_instance, 
        parameterized, param_key_model_fields, param_field_name, param_null
    ):
        """Test Model Field Parameter

        Ensure field parameter `param_field_name` has a value of `param_null`
        """


        if param_null == models.fields.NOT_PROVIDED:

            assert True

        else:

            assert getattr(model_instance._meta.get_field(param_field_name), 'null') == param_null



    def test_model_field_parameter_value_unique(self,
        model_instance, 
        parameterized, param_key_model_fields, param_field_name, param_unique
    ):
        """Test Model Field Parameter

        Ensure field parameter `param_field_name` has a value of `param_unique`
        """


        if param_unique == models.fields.NOT_PROVIDED:

            assert True

        else:

            assert getattr(model_instance._meta.get_field(param_field_name), 'unique') == param_unique



    def test_method_type___str__(self, model, model_instance ):
        """Test Method

        Ensure method `__str__` is of type `str`
        """

        if model._meta.abstract:

            pytest.xfail(reason = 'Model is an abstract model')


        assert type(model_instance.__str__()) is str



    def test_method_value_not_default___str__(self, model, model_instance ):
        """Test Method

        Ensure method `__str__` does not return the default value.
        """

        if model._meta.abstract:

            pytest.xfail(reason = 'Model is an abstract model')


        default_value = f'{model_instance._meta.object_name} object ({str(model_instance.id)})'

        assert model_instance.__str__() != default_value

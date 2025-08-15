import pytest

from django.db import models



@pytest.mark.unit
class ClassTestCases:
    """Class Common Test Suite

    This test suite contains all of the common tests for **ALL** Classes.

    To use this test suite you must define a fixture called `test_class` that
    contains the class to test.

    ## Test Setup

    define an attribute or property called `parameterized_class_attributes`
    that returns a dict of the following:

    ``` py
    '_audit_enabled': {
        'type': bool,    # TYpe the attribute should return
        'value': True,   # Value the attribute should return
    }
    ```

    **Note:** if the field does not exist, for the sub dict use `django.db.models.NOT_PROVIDED`

    """


    @property
    def parameterized_class_attributes(self):
        return {}


    @pytest.mark.regression
    def test_class_attribute_exists(self,
        test_class,
        parameterized, param_key_class_attributes, param_field_name, param_type
    ):
        """Test Class Attributes

        Ensure that field `param_field_name` exists within the model
        """

        if param_type == models.NOT_PROVIDED:

            pytest.xfail( reason = 'Class does not have attribute')

        assert hasattr(test_class, param_field_name)



    def test_class_attribute_type(self,
        test_class,
        parameterized, param_key_class_attributes, param_field_name, param_type
    ):
        """Test Class Attributes

        Ensure that field `param_field_name` has a type of `param_type`
        """

        if param_type == models.NOT_PROVIDED:

            pytest.xfail( reason = 'Class does not have attribute')


        if type(getattr(test_class, param_field_name)) is property:

            assert type( getattr(test_class, param_field_name).fget(test_class) ) is param_type, type( getattr(test_class, param_field_name).fget(test_class) )

        else:

            assert type(getattr(test_class, param_field_name)) is param_type, type(getattr(test_class, param_field_name))



    def test_class_attribute_value(self,
        test_class,
        parameterized, param_key_class_attributes, param_field_name, param_value
    ):
        """Test Class Attributes

        Ensure that field `param_field_name`has a value of `param_value`
        """

        if param_value == models.NOT_PROVIDED:

            pytest.xfail( reason = 'Class does not have attribute')


        if type(getattr(test_class, param_field_name)) is property:

            assert getattr(test_class, param_field_name).fget(test_class) == param_value, getattr(test_class, param_field_name).fget(test_class)

        else:

            assert getattr(test_class, param_field_name) == param_value, getattr(test_class, param_field_name)

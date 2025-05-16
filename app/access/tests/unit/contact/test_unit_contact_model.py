import pytest

from django.db import models

from access.models.contact import Contact
from access.tests.unit.person.test_unit_person_model import (
    PersonModelInheritedCases
)



class ContactModelTestCases(
    PersonModelInheritedCases,
):

    kwargs_create_item: dict = {
        'email': 'ipweird@unit.test',
    }

    sub_model_type = 'contact'
    """Sub Model Type

    sub-models must have this attribute defined in `ModelName.Meta.sub_model_type`
    """


    parameterized_fields: dict = {
        "email": {
            'field_type': models.fields.CharField,
            'field_parameter_default_exists': False,
            'field_parameter_verbose_name_type': str,
        },
        "directory": {
            'field_type': models.fields.BooleanField,
            'field_parameter_default_exists': True,
            'field_parameter_default_value': True,
            'field_parameter_verbose_name_type': str,
        }
    }



    def test_class_inherits_contact(self):
        """ Class inheritence

        TenancyObject must inherit SaveHistory
        """

        assert issubclass(self.model, Contact)


    # def test_attribute_value_history_app_label(self):
    #     """Attribute Type

    #     history_app_label has been set, override this test case with the value
    #     of attribute `history_app_label`
    #     """

    #     assert self.model.history_app_label == 'access'


    def test_attribute_value_history_model_name(self):
        """Attribute Type

        history_model_name has been set, override this test case with the value
        of attribute `history_model_name`
        """

        assert self.model.history_model_name == 'contact'



    def test_function_value_get_url(self):

        assert self.item.get_url() == '/api/v2/access/entity/contact/' + str(self.item.id)



class ContactModelInheritedCases(
    ContactModelTestCases,
):
    """Sub-Ticket Test Cases

    Test Cases for Ticket models that inherit from model Entity
    """

    kwargs_create_item: dict = {}

    model = None

    sub_model_type = None
    """Ticket Sub Model Type
    
    Ticket sub-models must have this attribute defined in `ModelNam.Meta.sub_model_type`
    """



class ContactModelPyTest(
    ContactModelTestCases,
):


    def test_function_value_get_related_model(self):
        """Function test

        Confirm function `get_related_model` is None for base model
        """

        assert self.item.get_related_model() is None

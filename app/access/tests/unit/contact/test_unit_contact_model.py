import pytest

from django.db import models

from access.models.contact import Contact
from access.tests.unit.person.test_unit_person_model import (
    PersonModelInheritedCases
)



@pytest.mark.model_contact
class ContactModelTestCases(
    PersonModelInheritedCases,
):

    sub_model_type = 'contact'
    """Sub Model Type

    sub-models must have this attribute defined in `ModelName.Meta.sub_model_type`
    """


    @property
    def parameterized_class_attributes(self):

        return {
            '_is_submodel': {
                'value': True
            },
            'url_model_name': {
                'type': str,
                'value': 'entity'
            }
        }


    @property
    def parameterized_fields(self):

        return {
            'directory': {
                'blank': True,
                'default': True,
                'field_type': models.BooleanField,
                'null': False,
                'unique': False,
            },
            'email': {
                'blank': False,
                'default': models.fields.NOT_PROVIDED,
                'field_type': models.EmailField,
                'null': False,
                'unique': True,
            },
        }



    def test_class_inherits_contact(self, model):
        """ Class inheritence

        TenancyObject must inherit SaveHistory
        """

        assert issubclass(model, Contact)



class ContactModelInheritedCases(
    ContactModelTestCases,
):
    """Sub-Ticket Test Cases

    Test Cases for Ticket models that inherit from model Entity
    """
    pass


@pytest.mark.module_access
class ContactModelPyTest(
    ContactModelTestCases,
):
    pass

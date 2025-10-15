import pytest

from django.db import models

from access.models.person import Person
from access.tests.unit.entity.test_unit_entity_model import (
    EntityModelInheritedCases
)



@pytest.mark.model_person
class PersonModelTestCases(
    EntityModelInheritedCases,
):


    sub_model_type = 'person'
    """Sub Model Type
    
    sub-models must have this attribute defined in `ModelName.Meta.sub_model_type`
    """


    @property
    def parameterized_class_attributes(self):

        return {
            '_is_submodel': {
                'value': True
            },
            '_linked_model_kwargs': {
                'type': tuple,
                'value': (
                    ( 'f_name', 'm_name', 'l_name', 'dob' ),
                    ( 'f_name', 'l_name', 'dob' ),
                    ( 'f_name', 'm_name', 'l_name' ),
                    ( 'f_name', 'l_name' ),
                ),
            },
            'url_model_name': {
                'type': str,
                'value': 'entity'
            }
        }


    @property
    def parameterized_fields(self):

        return {
            'f_name': {
                'blank': False,
                'default': models.fields.NOT_PROVIDED,
                'field_type': models.CharField,
                'length': 64,
                'null': False,
                'unique': False,
            },
            'm_name': {
                'blank': True,
                'default': models.fields.NOT_PROVIDED,
                'field_type': models.CharField,
                'length': 100,
                'null': True,
                'unique': False,
            },
            'l_name': {
                'blank': False,
                'default': models.fields.NOT_PROVIDED,
                'field_type': models.CharField,
                'length': 64,
                'null': False,
                'unique': False,
            },
            'dob': {
                'blank': True,
                'default': models.fields.NOT_PROVIDED,
                'field_type': models.DateField,
                'null': True,
                'unique': False,
            },
        }



    def test_class_inherits_person(self, model):
        """ Class inheritence

        TenancyObject must inherit SaveHistory
        """

        assert issubclass(model, Person)



class PersonModelInheritedCases(
    PersonModelTestCases,
):
    """Sub-Ticket Test Cases

    Test Cases for Ticket models that inherit from model Entity
    """
    pass



@pytest.mark.module_access
class PersonModelPyTest(
    PersonModelTestCases,
):
    pass

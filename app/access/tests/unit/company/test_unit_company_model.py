import pytest

from django.db import models

from access.models.company_base import Company
from access.tests.unit.entity.test_unit_entity_model import (
    EntityModelInheritedCases
)



@pytest.mark.model_company
class CompanyModelTestCases(
    EntityModelInheritedCases,
):


    sub_model_type = 'company'
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
            'name': {
                'blank': False,
                'default': models.fields.NOT_PROVIDED,
                'field_type': models.CharField,
                'length': 80,
                'null': False,
                'unique': False,
            }
        }



    def test_class_inherits_company(self, model):
        """ Class inheritence

        TenancyObject must inherit SaveHistory
        """

        assert issubclass(model, Company)



class CompanyModelInheritedCases(
    CompanyModelTestCases,
):
    """Sub-Ticket Test Cases

    Test Cases for Ticket models that inherit from model Entity
    """
    pass



@pytest.mark.module_access
class CompanyModelPyTest(
    CompanyModelTestCases,
):


    def test_function_value_get_related_model(self, model_instance):
        """Function test

        Confirm function `get_related_model` is None for base model
        """

        assert model_instance.get_related_model() is None

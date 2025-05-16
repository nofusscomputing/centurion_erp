import pytest

from django.db import models

from access.models.company_base import Company

from access.tests.unit.entity.test_unit_entity_model import (
    EntityModelInheritedCases
)



class CompanyModelTestCases(
    EntityModelInheritedCases,
):

    kwargs_create_item: dict = {
        'name': 'Ian',
    }

    sub_model_type = 'company'
    """Sub Model Type
    
    sub-models must have this attribute defined in `ModelName.Meta.sub_model_type`
    """


    parameterized_fields: dict = {
        "name": {
            'field_type': models.fields.CharField,
            'field_parameter_default_exists': False,
            'field_parameter_verbose_name_type': str,
        }
    }



    def test_class_inherits_company(self):
        """ Class inheritence

        TenancyObject must inherit SaveHistory
        """

        assert issubclass(self.model, Company)


    def test_attribute_value_history_app_label(self):
        """Attribute Type

        history_app_label has been set, override this test case with the value
        of attribute `history_app_label`
        """

        assert self.model.history_app_label == 'access'


    def test_attribute_value_history_model_name(self):
        """Attribute Type

        history_model_name has been set, override this test case with the value
        of attribute `history_model_name`
        """

        assert self.model.history_model_name == 'company'



    def test_function_value_get_url(self):

        assert self.item.get_url() == '/api/v2/access/entity/company/' + str(self.item.id)



class CompanyModelInheritedCases(
    CompanyModelTestCases,
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



class CompanyModelPyTest(
    CompanyModelTestCases,
):


    def test_function_value_get_related_model(self):
        """Function test

        Confirm function `get_related_model` is None for base model
        """

        assert self.item.get_related_model() is None

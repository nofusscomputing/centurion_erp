import pytest

from django.db import models

from access.tests.unit.contact.test_unit_contact_model import (
    ContactModelInheritedCases
)

from human_resources.models.employee import Employee



@pytest.mark.model_employee
class EmployeeModelTestCases(
    ContactModelInheritedCases,
):

    sub_model_type = 'employee'
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
            'employee_number': {
                'blank': False,
                'default': models.fields.NOT_PROVIDED,
                'field_type': models.IntegerField,
                'null': False,
                'unique': True,
            },
            'user': {
                'blank': True,
                'default': models.fields.NOT_PROVIDED,
                'field_type': models.OneToOneField,
                'null': True,
                'unique': True,
            },
        }



    def test_class_inherits_employee(self, model):
        """ Class inheritence

        TenancyObject must inherit SaveHistory
        """

        assert issubclass(model, Employee)



class EmployeeModelInheritedCases(
    EmployeeModelTestCases,
):
    """Sub-Ticket Test Cases

    Test Cases for Ticket models that inherit from model Entity
    """
    pass



@pytest.mark.module_human_resources
class EmployeeModelPyTest(
    EmployeeModelTestCases,
):
    pass

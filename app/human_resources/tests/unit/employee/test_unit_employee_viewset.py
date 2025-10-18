import pytest

from access.tests.unit.contact.test_unit_contact_viewset import (
    ContactViewsetInheritedCases
)

from human_resources.models.employee import Employee



@pytest.mark.model_employee
class ViewsetTestCases(
    ContactViewsetInheritedCases,
):

    @property
    def parameterized_class_attributes(self):
        return {
            'model': {
                'value': Employee
            }
        }



class EmployeeViewsetInheritedCases(
    ViewsetTestCases,
):
    pass


@pytest.mark.module_human_resources
class EmployeeViewsetPyTest(
    ViewsetTestCases,
):

    pass

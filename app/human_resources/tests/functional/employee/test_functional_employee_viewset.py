import pytest

from access.tests.functional.contact.test_functional_contact_viewset import (
    ContactViewsetInheritedCases
)

from human_resources.models.employee import Employee


@pytest.mark.model_employee
class ViewsetTestCases(
    ContactViewsetInheritedCases,
):
    pass



class EmployeeViewsetInheritedCases(
    ViewsetTestCases,
):
    pass



@pytest.mark.module_human_resources
class EmployeeViewsetPyTest(
    ViewsetTestCases,
):

    pass

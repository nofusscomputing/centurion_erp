import pytest

from django.test import TestCase

from access.tests.unit.contact.test_unit_contact_viewset import (
    ContactViewsetInheritedCases
)

from human_resources.models.employee import Employee



@pytest.mark.model_employee
class ViewsetTestCases(
    ContactViewsetInheritedCases,
):

    model: str = Employee



class EmployeeViewsetInheritedCases(
    ViewsetTestCases,
):
    """Sub-Entity Test Cases

    Test Cases for Entity models that inherit from model Employee
    """

    model: str = None
    """name of the model to test"""



@pytest.mark.module_human_resources
class EmployeeViewsetTest(
    ViewsetTestCases,
    TestCase,
):

    pass

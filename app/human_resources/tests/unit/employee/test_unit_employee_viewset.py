from django.test import TestCase

# from access.models.contact import Contact
from access.tests.unit.contact.test_unit_contact_viewset import (
    ContactViewsetInheritedCases
)

from human_resources.models.employee import Employee



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



class EmployeeViewsetTest(
    ViewsetTestCases,
    TestCase,
):

    pass

from django.test import TestCase

from access.tests.unit.contact.test_unit_contact_history_api_v2 import (
    ContactHistoryAPIInheritedCases
)

from human_resources.models.employee import Employee



class EmployeeModelHistoryAPITestCases(
    ContactHistoryAPIInheritedCases,
):
    """ Model Histoy Test Cases

    Test must be setup by creating object `kwargs_create_audit_object` with the
    attributes required to create the object.
    """

    audit_model = Employee

    kwargs_create_audit_object: dict = {
        'email': 'ipfunny@unit.test',
        'employee_number': 123456,
    }



class EmployeeHistoryAPIInheritedCases(
    EmployeeModelHistoryAPITestCases,
):
    """Sub-Entity Test Cases

    Test Cases for Entity models that inherit from model Contact
    """

    audit_model = None

    kwargs_create_audit_object: dict = None


    @classmethod
    def setUpTestData(self):

        self.kwargs_create_audit_object.update(
            super().kwargs_create_audit_object
        )

        super().setUpTestData()



class EmployeeModelHistoryAPITest(
    EmployeeModelHistoryAPITestCases,
    TestCase,
):

    pass

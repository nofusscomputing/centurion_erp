from django.test import TestCase

from access.tests.functional.contact.test_functional_contact_metadata import (
    ContactMetadataInheritedCases
)

from human_resources.models.employee import Employee



class EmployeeMetadataTestCases(
    ContactMetadataInheritedCases,
):

    add_data: dict = {
        'employee_number': 123456,
    }

    kwargs_create_item: dict = {
        'employee_number': 1234568,
    }

    kwargs_create_item_diff_org: dict = {
        'employee_number': 1234567,
    }

    model = Employee



class EmployeeMetadataInheritedCases(
    EmployeeMetadataTestCases,
):

    model = None

    kwargs_create_item: dict = {}

    kwargs_create_item_diff_org: dict = {}



class EmployeeMetadataTest(
    EmployeeMetadataTestCases,
    TestCase,

):
    pass
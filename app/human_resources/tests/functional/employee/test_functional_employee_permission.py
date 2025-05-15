from access.tests.functional.contact.test_functional_contact_permission import (
    ContactPermissionsAPIInheritedCases
)



class EmployeePermissionsAPITestCases(
    ContactPermissionsAPIInheritedCases,
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



class EmployeePermissionsAPIInheritedCases(
    EmployeePermissionsAPITestCases,
):

    add_data: dict = None

    kwargs_create_item: dict = None

    kwargs_create_item_diff_org: dict = None


class EmployeePermissionsAPIPyTest(
    EmployeePermissionsAPITestCases,
):

    pass

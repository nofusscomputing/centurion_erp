from django.test import TestCase

from access.tests.functional.contact.test_functional_contact_viewset import (
    ContactMetadataInheritedCases,
    ContactPermissionsAPIInheritedCases,
    ContactViewSetInheritedCases
)

from human_resources.models.employee import Employee



class ViewSetBase:

    add_data = {
        'email': 'ipfunny@unit.test',
        'employee_number': 123456,
    }

    kwargs_create_item_diff_org = {
        'email': 'ipstrange@unit.test',
        'employee_number': 1234567,
    }

    kwargs_create_item = {
        'email': 'ipweird@unit.test',
        'employee_number': 1234568,
    }

    model = Employee

    url_kwargs: dict = {}

    url_view_kwargs: dict = {}



class PermissionsAPITestCases(
    ViewSetBase,
    ContactPermissionsAPIInheritedCases,
):

    pass



class EmployeePermissionsAPIInheritedCases(
    PermissionsAPITestCases,
):

    add_data: dict = None

    model = None

    kwargs_create_item: dict = None

    kwargs_create_item_diff_org: dict = None


    @classmethod
    def setUpTestData(self):

        self.add_data.update(
            super().add_data
        )

        self.kwargs_create_item.update(
            super().kwargs_create_item
        )

        self.kwargs_create_item_diff_org.update(
            super().kwargs_create_item_diff_org
        )

        super().setUpTestData()



class EmployeePermissionsAPITest(
    PermissionsAPITestCases,
    TestCase,
):

    pass



class ViewSetTestCases(
    ViewSetBase,
    ContactViewSetInheritedCases,
):

    pass



class EmployeeViewSetInheritedCases(
    ViewSetTestCases,
):

    model = None

    kwargs_create_item: dict = None

    kwargs_create_item_diff_org: dict = None


    @classmethod
    def setUpTestData(self):

        self.kwargs_create_item.update(
            super().kwargs_create_item
        )

        self.kwargs_create_item_diff_org.update(
            super().kwargs_create_item_diff_org
        )

        super().setUpTestData()



class EmployeeViewSetTest(
    ViewSetTestCases,
    TestCase,
):

    pass



class MetadataTestCases(
    ViewSetBase,
    ContactMetadataInheritedCases,
):

    pass



class EmployeeMetadataInheritedCases(
    MetadataTestCases,
):

    model = None

    kwargs_create_item: dict = None

    kwargs_create_item_diff_org: dict = None


    @classmethod
    def setUpTestData(self):

        self.kwargs_create_item.update(
            super().kwargs_create_item
        )

        self.kwargs_create_item_diff_org.update(
            super().kwargs_create_item_diff_org
        )

        super().setUpTestData()



class EmployeeMetadataTest(
    MetadataTestCases,
    TestCase,

):

    pass

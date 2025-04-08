from django.test import TestCase

from access.models.contact import Contact
from access.tests.functional.person.test_functional_person_viewset import (
    PersonMetadataInheritedCases,
    PersonPermissionsAPIInheritedCases,
    PersonViewSetInheritedCases
)



class ViewSetBase:

    add_data = {
        'email': 'ipfunny@unit.test',
    }

    kwargs_create_item_diff_org = {
        'email': 'ipstrange@unit.test',
    }

    kwargs_create_item = {
        'email': 'ipweird@unit.test',
    }

    model = Contact

    url_kwargs: dict = {}

    url_view_kwargs: dict = {}



class PermissionsAPITestCases(
    ViewSetBase,
    PersonPermissionsAPIInheritedCases,
):

    pass



class ContactPermissionsAPIInheritedCases(
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



class ContactPermissionsAPITest(
    PermissionsAPITestCases,
    TestCase,
):

    pass



class ViewSetTestCases(
    ViewSetBase,
    PersonViewSetInheritedCases,
):

    pass



class ContactViewSetInheritedCases(
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



class ContactViewSetTest(
    ViewSetTestCases,
    TestCase,
):

    pass



class MetadataTestCases(
    ViewSetBase,
    PersonMetadataInheritedCases,
):

    pass



class ContactMetadataInheritedCases(
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



class ContactMetadataTest(
    MetadataTestCases,
    TestCase,

):

    pass

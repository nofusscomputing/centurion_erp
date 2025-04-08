from django.test import TestCase

from access.models.person import Person
from access.tests.functional.entity.test_functional_entity_viewset import (
    EntityMetadataInheritedCases,
    EntityPermissionsAPIInheritedCases,
    EntityViewSetInheritedCases
)



class ViewSetBase:

    add_data = {
        'f_name': 'Ian',
        'm_name': 'Peter',
        'l_name': 'Strange',
        'dob': '2025-04-08',
    }

    kwargs_create_item_diff_org = {
        'f_name': 'Ian',
        'm_name': 'Peter',
        'l_name': 'Funny',
        'dob': '2025-04-08',
    }

    kwargs_create_item = {
        'f_name': 'Ian',
        'm_name': 'Peter',
        'l_name': 'Weird',
        'dob': '2025-04-08',
    }

    model = Person

    url_kwargs: dict = {}

    url_view_kwargs: dict = {}



class PermissionsAPITestCases(
    ViewSetBase,
    EntityPermissionsAPIInheritedCases,
):

    pass



class PersonPermissionsAPIInheritedCases(
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



class PersonPermissionsAPITest(
    PermissionsAPITestCases,
    TestCase,
):

    pass



class ViewSetTestCases(
    ViewSetBase,
    EntityViewSetInheritedCases,
):

    pass



class PersonViewSetInheritedCases(
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



class PersonViewSetTest(
    ViewSetTestCases,
    TestCase,
):

    pass



class MetadataTestCases(
    ViewSetBase,
    EntityMetadataInheritedCases,
):

    pass



class PersonMetadataInheritedCases(
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



class PersonMetadataTest(
    MetadataTestCases,
    TestCase,

):

    pass

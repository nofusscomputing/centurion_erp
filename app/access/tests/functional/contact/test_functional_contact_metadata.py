from django.test import TestCase

from access.models.contact import Contact

from access.tests.functional.person.test_functional_person_metadata import (
    PersonMetadataInheritedCases
)



class ContactMetadataTestCases(
    PersonMetadataInheritedCases,
):

    add_data: dict = {
        'email': 'ipfunny@unit.test',
    }

    kwargs_create_item: dict = {
        'email': 'ipweird@unit.test',
    }

    kwargs_create_item_diff_org: dict = {
        'email': 'ipstrange@unit.test',
    }

    model = Contact




class ContactMetadataInheritedCases(
    ContactMetadataTestCases,
):

    model = None

    kwargs_create_item: dict = {}

    kwargs_create_item_diff_org: dict = {}


    @classmethod
    def setUpTestData(self):

        self.kwargs_create_item = {
            **super().kwargs_create_item,
            **self.kwargs_create_item
        }

        self.kwargs_create_item_diff_org = {
            **super().kwargs_create_item_diff_org,
            **self.kwargs_create_item_diff_org
        }

        super().setUpTestData()



class ContactMetadataTest(
    ContactMetadataTestCases,
    TestCase,

):
    pass
from django.test import TestCase

from access.models.contact import Contact
from access.tests.functional.person.test_functional_person_viewset import (
    PersonViewSetInheritedCases
)



class ViewSetTestCases(
    PersonViewSetInheritedCases,
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



class ContactViewSetInheritedCases(
    ViewSetTestCases,
):

    model = None


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



class ContactViewSetTest(
    ViewSetTestCases,
    TestCase,
):
    pass

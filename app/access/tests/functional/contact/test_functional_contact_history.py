from django.test import TestCase

from access.models.contact import Contact
from access.tests.functional.person.test_functional_person_history import (
    PersonHistoryInheritedCases
)



class ContactTestCases(
    PersonHistoryInheritedCases,
):

    field_name = 'model_notes'

    kwargs_create_obj: dict = {
        'email': 'ipfunny@unit.test',
    }

    kwargs_delete_obj: dict = {
        'email': 'ipweird@unit.test',
    }

    model = Contact



class ContactHistoryInheritedCases(
    ContactTestCases,
):

    model = None
    """Entity model to test"""

    kwargs_create_obj: dict = None

    kwargs_delete_obj: dict = None


    @classmethod
    def setUpTestData(self):

        self.kwargs_create_obj.update(
            super().kwargs_create_obj
        )

        self.kwargs_delete_obj.update(
            super().kwargs_delete_obj
        )

        super().setUpTestData()



class ContactHistoryTest(
    ContactTestCases,
    TestCase,
):

    pass

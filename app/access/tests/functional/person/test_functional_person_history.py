from django.test import TestCase

from access.models.person import Person
from access.tests.functional.entity.test_functional_entity_history import (
    EntityHistoryInheritedCases
)



class PersonTestCases(
    EntityHistoryInheritedCases,
):

    field_name = 'model_notes'

    kwargs_create_obj: dict = {
        'f_name': 'Ian',
        'm_name': 'Peter',
        'l_name': 'Funny',
        'dob': '2025-04-08',
    }

    kwargs_delete_obj: dict = {
        'f_name': 'Ian',
        'm_name': 'Peter',
        'l_name': 'Weird',
        'dob': '2025-04-08',
    }

    model = Person


class PersonHistoryInheritedCases(
    PersonTestCases,
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



class PersonHistoryTest(
    PersonTestCases,
    TestCase,
):

    pass

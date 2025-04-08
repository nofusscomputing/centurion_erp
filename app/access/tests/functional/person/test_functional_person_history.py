from django.test import TestCase

from access.models.person import Person
from access.tests.functional.entity.test_functional_entity_history import EntityHistoryInheritedCases



class PersonTestCases(
    EntityHistoryInheritedCases,
):

    field_name = 'model_notes'

    kwargs_create_obj: dict = {}

    kwargs_delete_obj: dict = {}

    model = Person

    @classmethod
    def setUpTestData(self):

        self.kwargs_create_obj.update({
            'f_name': 'Ian',
            'm_name': 'Peter',
            'l_name': 'Funny',
            'dob': '2025-04-08',
        })

        self.kwargs_delete_obj.update({
            'f_name': 'Ian',
            'm_name': 'Peter',
            'l_name': 'Weird',
            'dob': '2025-04-08',
        })

        super().setUpTestData()



class PersonHistoryInheritedCases(
    PersonTestCases,
):

    model = None
    """Entity model to test"""

    kwargs_create_obj: dict = None

    kwargs_delete_obj: dict = None



class PersonHistoryTest(
    PersonTestCases,
    TestCase,
):

    pass

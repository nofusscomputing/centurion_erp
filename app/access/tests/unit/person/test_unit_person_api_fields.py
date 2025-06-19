import pytest

from access.tests.unit.entity.test_unit_entity_api_fields import (
    EntityAPIInheritedCases
)



@pytest.mark.model_person
class PersonAPITestCases(
    EntityAPIInheritedCases,
):

    parameterized_test_data = {
        'f_name': {
            'expected': str
        },
        'm_name': {
            'expected': str
        },
        'l_name': {
            'expected': str
        },
        'dob': {
            'expected': str
        }
    }

    kwargs_create_item: dict = {
        'entity_type': 'person',
        'f_name': 'Ian',
        'm_name': 'Peter',
        'l_name': 'Funny',
        'dob': '2025-04-08',
    }



class PersonAPIInheritedCases(
    PersonAPITestCases,
):

    kwargs_create_item: dict = None

    model = None



@pytest.mark.module_access
class PersonAPIPyTest(
    PersonAPITestCases,
):

    pass

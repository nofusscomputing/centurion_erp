import pytest

from access.tests.unit.person.test_unit_person_api_fields import (
    PersonAPIInheritedCases
)



@pytest.mark.model_contact
class ContactAPITestCases(
    PersonAPIInheritedCases,
):

    parameterized_test_data = {
        'email': {
            'expected': str
        },
        'directory': {
            'expected': bool
        }
    }

    kwargs_create_item: dict = {
        'email': 'ipfunny@unit.test',
    }



class ContactAPIInheritedCases(
    ContactAPITestCases,
):

    kwargs_create_item: dict = None

    model = None



@pytest.mark.module_access
class ContactAPIPyTest(
    ContactAPITestCases,
):

    pass

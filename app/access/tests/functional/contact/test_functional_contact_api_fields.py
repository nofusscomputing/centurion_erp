import pytest

from access.tests.functional.person.test_functional_person_api_fields import (
    PersonAPIInheritedCases
)



@pytest.mark.model_contact
class ContactAPITestCases(
    PersonAPIInheritedCases,
):

    @property
    def parameterized_api_fields(self): 

        return {
            'email': {
                'expected': str
            },
            'directory': {
                'expected': bool
            }
        }



class ContactAPIInheritedCases(
    ContactAPITestCases,
):

    pass



@pytest.mark.module_access
class ContactAPIPyTest(
    ContactAPITestCases,
):

    pass

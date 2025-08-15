import pytest

from access.tests.functional.entity.test_functional_entity_api_fields import (
    EntityAPIInheritedCases
)



@pytest.mark.model_person
class PersonAPITestCases(
    EntityAPIInheritedCases,
):

    property
    def parameterized_api_fields(self): 

        return {
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



class PersonAPIInheritedCases(
    PersonAPITestCases,
):

    pass



@pytest.mark.module_access
class PersonAPIPyTest(
    PersonAPITestCases,
):

    pass

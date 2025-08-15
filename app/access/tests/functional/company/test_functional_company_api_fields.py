import pytest

from access.tests.functional.entity.test_functional_entity_api_fields import (
    EntityAPIInheritedCases
)



@pytest.mark.model_company
class CompanyAPITestCases(
    EntityAPIInheritedCases,
):

    @property
    def parameterized_api_fields(self): 

        return {
            'name': {
                'expected': str
            }
        }


class CompanyAPIInheritedCases(
    CompanyAPITestCases,
):
    pass



@pytest.mark.module_access
class CompanyAPIPyTest(
    CompanyAPITestCases,
):

    pass

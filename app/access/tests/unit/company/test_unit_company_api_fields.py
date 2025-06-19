import pytest

from access.tests.unit.entity.test_unit_entity_api_fields import (
    EntityAPIInheritedCases
)



@pytest.mark.model_company
class CompanyAPITestCases(
    EntityAPIInheritedCases,
):

    parameterized_test_data = {
        'name': {
            'expected': str
        }
    }

    kwargs_create_item: dict = {
        'name': 'Ian'
    }



class CompanyAPIInheritedCases(
    CompanyAPITestCases,
):

    kwargs_create_item: dict = None

    model = None



@pytest.mark.module_access
class CompanyAPIPyTest(
    CompanyAPITestCases,
):

    pass

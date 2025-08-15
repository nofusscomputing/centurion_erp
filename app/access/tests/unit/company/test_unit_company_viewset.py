import pytest

from access.models.company_base import Company
from access.tests.unit.entity.test_unit_entity_viewset import (
    EntityViewsetInheritedCases
)



@pytest.mark.model_company
class ViewsetTestCases(
    EntityViewsetInheritedCases,
):


    @property
    def parameterized_class_attributes(self):
        return {
            'model': {
                'value': Company
            }
        }



class CompanyViewsetInheritedCases(
    ViewsetTestCases,
):
    """Sub-Entity Test Cases

    Test Cases for Entity models that inherit from model Company
    """

    pass



@pytest.mark.module_access
class CompanyViewsetPyTest(
    ViewsetTestCases,
):

    pass

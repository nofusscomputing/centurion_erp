import pytest

from access.tests.functional.entity.test_functional_entity_viewset import (
    EntityViewsetInheritedCases
)



@pytest.mark.model_company
class ViewsetTestCases(
    EntityViewsetInheritedCases,
):
    pass


class CompanyViewsetInheritedCases(
    ViewsetTestCases,
):

    pass



@pytest.mark.module_access
class CompanyViewsetPyTest(
    ViewsetTestCases,
):

    pass

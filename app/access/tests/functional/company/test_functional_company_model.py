import pytest

from access.tests.functional.entity.test_functional_entity_model import EntityModelInheritedCases



@pytest.mark.model_company
class CompanyModelTestCases(
    EntityModelInheritedCases
):
    pass


class CompanyModelInheritedCases(
    CompanyModelTestCases,
):
    pass


@pytest.mark.module_access
class CompanyModelPyTest(
    CompanyModelTestCases,
):
    pass

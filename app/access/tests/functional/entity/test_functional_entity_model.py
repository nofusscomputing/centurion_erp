import pytest

from core.tests.functional.centurion_abstract.test_functional_centurion_abstract_model import (
    CenturionAbstractTenancyModelInheritedCases
)



@pytest.mark.model_entity
class EntityModelTestCases(
    CenturionAbstractTenancyModelInheritedCases
):
    pass



class EntityModelInheritedCases(
    EntityModelTestCases,
):
    pass



@pytest.mark.module_access
class EntityModelPyTest(
    EntityModelTestCases,
):
    pass

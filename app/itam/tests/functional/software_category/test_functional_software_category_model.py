import pytest

from core.tests.functional.centurion_abstract.test_functional_centurion_abstract_model import (
    CenturionAbstractTenancyModelInheritedCases
)



@pytest.mark.model_softwarecategory
class SoftwareCategoryModelTestCases(
    CenturionAbstractTenancyModelInheritedCases
):
    pass



class SoftwareCategoryModelInheritedCases(
    SoftwareCategoryModelTestCases,
):
    pass



@pytest.mark.module_itam
class SoftwareCategoryModelPyTest(
    SoftwareCategoryModelTestCases,
):
    pass

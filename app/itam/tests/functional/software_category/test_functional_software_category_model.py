import pytest

from core.tests.functional.centurion_abstract.test_functional_centurion_abstract_model import (
    CenturionAbstractModelInheritedCases
)



@pytest.mark.model_softwarecategory
class SoftwareCategoryModelTestCases(
    CenturionAbstractModelInheritedCases
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

import pytest

from core.tests.functional.centurion_abstract.test_functional_centurion_abstract_model import (
    CenturionAbstractTenancyModelInheritedCases
)



@pytest.mark.model_knowledgebasecategory
class knowledgeBaseCategoryModelTestCases(
    CenturionAbstractTenancyModelInheritedCases
):
    pass



class knowledgeBaseCategoryModelInheritedCases(
    knowledgeBaseCategoryModelTestCases,
):
    pass



@pytest.mark.module_assistance
class knowledgeBaseCategoryModelPyTest(
    knowledgeBaseCategoryModelTestCases,
):
    pass

import pytest

from core.tests.functional.centurion_abstract.test_functional_centurion_abstract_model import (
    CenturionAbstractTenancyModelInheritedCases
)



@pytest.mark.model_knowledgebase
class knowledgeBaseModelTestCases(
    CenturionAbstractTenancyModelInheritedCases
):
    pass



class knowledgeBaseModelInheritedCases(
    knowledgeBaseModelTestCases,
):
    pass



@pytest.mark.module_assistance
class knowledgeBaseModelPyTest(
    knowledgeBaseModelTestCases,
):
    pass

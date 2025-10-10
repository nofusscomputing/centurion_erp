import pytest

from core.tests.functional.centurion_abstract.test_functional_centurion_abstract_model import (
    CenturionAbstractTenancyModelInheritedCases
)



@pytest.mark.model_externallink
class ExternalLinkModelTestCases(
    CenturionAbstractTenancyModelInheritedCases
):
    pass



class ExternalLinkModelInheritedCases(
    ExternalLinkModelTestCases,
):
    pass



@pytest.mark.module_settings
class ExternalLinkModelPyTest(
    ExternalLinkModelTestCases,
):
    pass

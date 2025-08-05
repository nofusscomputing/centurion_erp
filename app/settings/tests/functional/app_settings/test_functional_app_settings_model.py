import pytest

from core.tests.functional.centurion_abstract.test_functional_centurion_abstract_model import (
    CenturionAbstractModelInheritedCases
)



@pytest.mark.model_appsettings
class AppSettingsModelTestCases(
    CenturionAbstractModelInheritedCases
):
    pass



class AppSettingsModelInheritedCases(
    AppSettingsModelTestCases,
):
    pass



@pytest.mark.module_settings
class AppSettingsModelPyTest(
    AppSettingsModelTestCases,
):
    pass

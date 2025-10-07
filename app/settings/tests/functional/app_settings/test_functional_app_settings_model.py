import pytest

from core.tests.functional.centurion_abstract.test_functional_centurion_abstract_model import (
    CenturionAbstractTenancyModelInheritedCases
)



@pytest.mark.model_appsettings
class AppSettingsModelTestCases(
    CenturionAbstractTenancyModelInheritedCases
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

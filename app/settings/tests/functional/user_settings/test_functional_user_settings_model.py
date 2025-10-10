import pytest

from core.tests.functional.centurion_abstract.test_functional_centurion_abstract_model import (
    CenturionAbstractTenancyModelInheritedCases
)



@pytest.mark.model_usersettings
class UserSettingsModelTestCases(
    CenturionAbstractTenancyModelInheritedCases
):
    pass



class UserSettingsModelInheritedCases(
    UserSettingsModelTestCases,
):
    pass



@pytest.mark.module_settings
class UserSettingsModelPyTest(
    UserSettingsModelTestCases,
):
    pass

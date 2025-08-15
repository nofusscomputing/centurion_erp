import pytest

from core.tests.functional.centurion_abstract.test_functional_centurion_abstract_model import (
    CenturionAbstractModelInheritedCases
)



@pytest.mark.model_usersettings
class UserSettingsModelTestCases(
    CenturionAbstractModelInheritedCases
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

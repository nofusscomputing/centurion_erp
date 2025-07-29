import pytest

from core.tests.functional.centurion_abstract.test_functional_centurion_abstract_model import (
    CenturionAbstractModelInheritedCases
)



@pytest.mark.model_configgroups
class ConfigGroupsModelTestCases(
    CenturionAbstractModelInheritedCases
):
    pass



class ConfigGroupsModelInheritedCases(
    ConfigGroupsModelTestCases,
):
    pass



@pytest.mark.module_config_management
class ConfigGroupsModelPyTest(
    ConfigGroupsModelTestCases,
):
    pass

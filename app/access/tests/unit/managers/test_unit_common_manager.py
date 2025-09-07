import pytest



@pytest.mark.manager
@pytest.mark.manager_common
@pytest.mark.unit
class CommonManagerTestCases:
    pass

class CommonManagerInheritedCases(
    CommonManagerTestCases
):
    pass

@pytest.mark.module_access
class CommonManagerPytest(
    CommonManagerTestCases
):
    pass

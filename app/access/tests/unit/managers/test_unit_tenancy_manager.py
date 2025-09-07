import pytest



@pytest.mark.manager
@pytest.mark.manager_tenancy
class TenancyManagerTestCases(
    CommonManagerInheritedCases
):

    pass


class TenancyManagerInheritedCases(
    TenancyManagerTestCases
):
    pass


@pytest.mark.module_access
class TenancyManagerPytest(
    TenancyManagerTestCases
):
    pass

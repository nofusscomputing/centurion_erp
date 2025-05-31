import pytest

from api.tests.functional.test_functional_permissions_api import (
    APIPermissionsInheritedCases,
)


@pytest.mark.model_gitgroup
class GitGroupPermissionsAPITestCases(
    APIPermissionsInheritedCases,
):

    pass



class GitGroupPermissionsAPIInheritedCases(
    GitGroupPermissionsAPITestCases,
):
    pass


class GitGroupPermissionsAPIPyTest(
    GitGroupPermissionsAPITestCases,
):

    pass

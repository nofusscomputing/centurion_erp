import pytest

from access.tests.functional.entity.test_functional_entity_viewset import (
    EntityViewsetInheritedCases
)



@pytest.mark.model_person
class ViewsetTestCases(
    EntityViewsetInheritedCases,
):
    pass



class PersonViewsetInheritedCases(
    ViewsetTestCases,
):
    pass



@pytest.mark.module_access
class PersonViewsetPyTest(
    ViewsetTestCases,
):

    pass

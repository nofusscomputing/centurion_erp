import pytest

from access.tests.functional.entity.test_functional_entity_model import EntityModelInheritedCases



@pytest.mark.model_person
class PersonModelTestCases(
    EntityModelInheritedCases
):
    pass



class PersonModelInheritedCases(
    PersonModelTestCases,
):
    pass



@pytest.mark.module_access
class PersonModelPyTest(
    PersonModelTestCases,
):
    pass

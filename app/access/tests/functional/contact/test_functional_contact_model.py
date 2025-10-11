import pytest

from access.tests.functional.person.test_functional_person_model import PersonModelInheritedCases



@pytest.mark.model_contact
class ContactModelTestCases(
    PersonModelInheritedCases
):
    pass



class ContactModelInheritedCases(
    ContactModelTestCases,
):
    pass



@pytest.mark.module_access
class ContactModelPyTest(
    ContactModelTestCases,
):
    pass

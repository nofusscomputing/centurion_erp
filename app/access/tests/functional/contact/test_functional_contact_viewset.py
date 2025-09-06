import pytest

from access.tests.functional.person.test_functional_person_viewset import (
    PersonViewsetInheritedCases
)



@pytest.mark.model_contact
class ViewsetTestCases(
    PersonViewsetInheritedCases,
):
    pass



class ContactViewsetInheritedCases(
    ViewsetTestCases,
):

    pass



@pytest.mark.module_access
class ContactViewsetPyTest(
    ViewsetTestCases,
):

    pass

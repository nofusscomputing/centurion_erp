import pytest

from access.models.contact import Contact
from access.tests.unit.person.test_unit_person_viewset import (
    PersonViewsetInheritedCases
)



@pytest.mark.model_contact
class ViewsetTestCases(
    PersonViewsetInheritedCases,
):


    @property
    def parameterized_class_attributes(self):
        return {
            'model': {
                'value': Contact
            }
        }



class ContactViewsetInheritedCases(
    ViewsetTestCases,
):
    """Sub-Entity Test Cases

    Test Cases for Entity models that inherit from model Contact
    """

    pass



@pytest.mark.module_access
class ContactViewsetPyTest(
    ViewsetTestCases,
):

    pass

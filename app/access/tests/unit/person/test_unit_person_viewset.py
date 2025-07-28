import pytest

from access.models.person import Person
from access.tests.unit.entity.test_unit_entity_viewset import (
    EntityViewsetInheritedCases
)



@pytest.mark.model_person
class ViewsetTestCases(
    EntityViewsetInheritedCases,
):


    @property
    def parameterized_class_attributes(self):
        return {
            'model': {
                'value': Person
            }
        }




class PersonViewsetInheritedCases(
    ViewsetTestCases,
):
    """Sub-Entity Test Cases

    Test Cases for Entity models that inherit from model Person
    """

    pass



@pytest.mark.module_access
class PersonViewsetPyTest(
    ViewsetTestCases,
):

    pass

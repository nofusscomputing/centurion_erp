import pytest

from django.test import TestCase

from access.models.person import Person
from access.tests.unit.entity.test_unit_entity_viewset import (
    EntityViewsetInheritedCases
)



@pytest.mark.model_person
class ViewsetTestCases(
    EntityViewsetInheritedCases,
):

    model: str = Person



class PersonViewsetInheritedCases(
    ViewsetTestCases,
):
    """Sub-Entity Test Cases

    Test Cases for Entity models that inherit from model Person
    """

    model: str = None
    """name of the model to test"""



@pytest.mark.module_access
class PersonViewsetTest(
    ViewsetTestCases,
    TestCase,
):

    pass

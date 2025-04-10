from django.test import TestCase

from access.models.contact import Contact
from access.tests.unit.entity.test_unit_entity_viewset import (
    EntityViewsetInheritedCases
)



class ViewsetTestCases(
    EntityViewsetInheritedCases,
):

    model: str = Contact



class ContactViewsetInheritedCases(
    ViewsetTestCases,
):
    """Sub-Entity Test Cases

    Test Cases for Entity models that inherit from model Contact
    """

    model: str = None
    """name of the model to test"""



class ContactViewsetTest(
    ViewsetTestCases,
    TestCase,
):

    pass

from django.test import TestCase

from access.models.person import Person
from access.tests.unit.entity.test_unit_entity_model import (
    EntityModelInheritedCases
)



class ModelTestCases(
    EntityModelInheritedCases,
):

    model = None

    kwargs_item_create: dict = None



class PersonModelInheritedCases(
    ModelTestCases,
):
    """Sub-Entity Test Cases

    Test Cases for Entity models that inherit from model Person
    """

    kwargs_item_create: dict = None

    model = None



class PersonModelTest(
    ModelTestCases,
    TestCase,
):

    model = Person

    kwargs_item_create: dict = {
        'f_name': 'Ian',
        'm_name': 'Peter',
        'l_name': 'Funny',
        'dob': '2025-04-08',
    }

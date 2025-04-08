from django.test import TestCase

from access.models.person import Person
from access.tests.unit.entity.test_unit_entity_access_tenancy_object import (
    EntityTenancyObjectInheritedCases,
)

class TenancyObjectTestCases(
    EntityTenancyObjectInheritedCases,
):

    model = Person


class PersonTenancyObjectInheritedCases(
    TenancyObjectTestCases,
):
    """Sub-Entity Test Cases

    Test Cases for Entity models that inherit from model Person
    """

    model = None



class PersonTenancyObjectTest(
    TenancyObjectTestCases,
    TestCase,
):

    pass

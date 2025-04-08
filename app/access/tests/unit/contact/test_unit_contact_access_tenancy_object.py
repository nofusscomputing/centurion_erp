from django.test import TestCase

from access.models.contact import Contact
from access.tests.unit.person.test_unit_person_access_tenancy_object import (
    PersonTenancyObjectInheritedCases,
)

class TenancyObjectTestCases(
    PersonTenancyObjectInheritedCases,
):

    model = Contact


class ContactTenancyObjectInheritedCases(
    TenancyObjectTestCases,
):
    """Sub-Entity Test Cases

    Test Cases for Entity models that inherit from model Contact
    """

    model = None



class ContactTenancyObjectTest(
    TenancyObjectTestCases,
    TestCase,
):

    pass

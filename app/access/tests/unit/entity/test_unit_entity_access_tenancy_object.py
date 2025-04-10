from django.test import TestCase

from access.models.entity import Entity
from access.tests.abstract.tenancy_object import TenancyObject



class TenancyObjectTestCases(
    TenancyObject,
):

    model = None



class EntityTenancyObjectInheritedCases(
    TenancyObjectTestCases,
):

    model = None



class EntityTenancyObjectTest(
    TenancyObjectTestCases,
    TestCase,
):

    model = Entity

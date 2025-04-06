from django.test import TestCase

from access.models.role import Role
from access.tests.abstract.tenancy_object import TenancyObject



class TenancyObjectTestCases(
    TenancyObject,
):

    model = None



class RoleTenancyObjectTest(
    TenancyObjectTestCases,
    TestCase,
):

    model = Role

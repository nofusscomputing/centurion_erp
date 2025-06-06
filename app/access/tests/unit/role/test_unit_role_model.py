from django.test import TestCase

from access.models.role import Role

from centurion.tests.unit.test_unit_models import (
    TenancyObjectInheritedCases
)



class RoleModelTestCases(
    TenancyObjectInheritedCases,
):

    model = None

    kwargs_item_create: dict = None



class RoleModelTest(
    RoleModelTestCases,
    TestCase,
):

    model = Role

    kwargs_item_create: dict = {
        'name': 'a role'
    }

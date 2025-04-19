from django.test import TestCase

from access.models.role import Role

from app.tests.unit.test_unit_models import (
    TenancyObjectInheritedCases
)



class RoleModelTestCases(
    TenancyObjectInheritedCases,
):

    model = None

    kwargs_item_create: dict = None


    def test_field_exist_is_global(self):
        """Test model field not used

        object must not be settable as a global object

        Attribute `is_global` must be defined as None
        """

        assert self.model.is_global is None



class RoleModelTest(
    RoleModelTestCases,
    TestCase,
):

    model = Role

    kwargs_item_create: dict = {
        'name': 'a role'
    }

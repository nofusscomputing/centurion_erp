from django.test import TestCase

from centurion.tests.unit.test_unit_models import (
    TenancyObjectInheritedCases
)

from core.models.manufacturer import Manufacturer


class ManufacturerModelTestCases(
    TenancyObjectInheritedCases,
):

    kwargs_item_create = {
        'name': 'man'
    }

    model = Manufacturer



class ManufacturerModelTest(
    ManufacturerModelTestCases,
    TestCase,
):

    pass

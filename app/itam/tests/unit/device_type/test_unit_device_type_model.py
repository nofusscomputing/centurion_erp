from django.test import TestCase

from centurion.tests.unit.test_unit_models import (
    TenancyObjectInheritedCases
)

from itam.models.device import DeviceType


class DeviceTypeModel(
    TenancyObjectInheritedCases,
    TestCase,
):

    model = DeviceType

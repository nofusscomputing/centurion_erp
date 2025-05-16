from django.test import TestCase

from centurion.tests.unit.test_unit_models import (
    TenancyObjectInheritedCases
)

from itam.models.software import SoftwareCategory



class SoftwareCategoryModel(
    TenancyObjectInheritedCases,
    TestCase,
):

    model = SoftwareCategory

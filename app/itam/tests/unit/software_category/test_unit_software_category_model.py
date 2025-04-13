from django.test import TestCase

from app.tests.unit.test_unit_models import (
    TenancyObjectInheritedCases
)

from itam.models.software import SoftwareCategory



class SoftwareCategoryModel(
    TenancyObjectInheritedCases,
    TestCase,
):

    model = SoftwareCategory

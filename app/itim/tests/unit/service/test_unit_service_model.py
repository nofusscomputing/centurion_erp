from django.test import TestCase

from app.tests.unit.test_unit_models import (
    TenancyObjectInheritedCases
)

from itim.models.services import Service



class ServiceModel(
    TenancyObjectInheritedCases,
    TestCase,
):

    model = Service

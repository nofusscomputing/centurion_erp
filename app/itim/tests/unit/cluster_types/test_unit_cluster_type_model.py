from django.test import TestCase

from app.tests.unit.test_unit_models import (
    TenancyObjectInheritedCases
)

from itim.models.clusters import ClusterType



class ClusterTypeModel(
    TenancyObjectInheritedCases,
    TestCase,
):

    model = ClusterType

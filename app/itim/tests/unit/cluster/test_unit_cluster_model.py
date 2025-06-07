from django.test import TestCase

from centurion.tests.unit.test_unit_models import (
    TenancyObjectInheritedCases
)

from itim.models.clusters import Cluster



class ClusterModel(
    TenancyObjectInheritedCases,
    TestCase,
):

    model = Cluster

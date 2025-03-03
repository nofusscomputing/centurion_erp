from django.test import TestCase

from access.tests.abstract.tenancy_object import TenancyObject

from devops.models.feature_flag import FeatureFlag



class TenancyObject(
    TestCase,
    TenancyObject
):

    model = FeatureFlag

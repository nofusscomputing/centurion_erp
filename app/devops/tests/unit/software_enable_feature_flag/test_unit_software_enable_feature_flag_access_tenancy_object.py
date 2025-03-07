from django.test import TestCase

from access.tests.abstract.tenancy_object import TenancyObject

from devops.models.software_enable_feature_flag import SoftwareEnableFeatureFlag



class TenancyObject(
    TestCase,
    TenancyObject
):

    model = SoftwareEnableFeatureFlag

    should_model_history_be_saved: bool = False

from django.test import TestCase

from core.tests.abstract.test_functional_history import HistoryEntriesCommon

from devops.models.feature_flag_history import FeatureFlag, FeatureFlagHistory
from devops.models.software_enable_feature_flag import SoftwareEnableFeatureFlag

from itam.models.software import Software



class History(
    HistoryEntriesCommon,
    TestCase,
):

    model = FeatureFlag

    history_model = FeatureFlagHistory


    @classmethod
    def setUpTestData(self):

        super().setUpTestData()


        software = Software.objects.create(
            organization = self.organization,
            name = 'soft',
        )

        SoftwareEnableFeatureFlag.objects.create(
            organization = self.organization,
            software = software,
            enabled = True
        )

        self.obj = self.model.objects.create(
            organization = self.organization,
            name = self.field_value_original,
            software = software
        )

        self.obj_delete = self.model.objects.create(
            organization = self.organization,
            name = self.field_value_delete,
            software = software
        )

        self.call_the_banners()

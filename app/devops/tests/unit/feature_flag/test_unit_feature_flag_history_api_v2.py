from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

from core.tests.abstract.test_unit_model_history_api_v2 import PrimaryModelHistoryAPI

from devops.models.feature_flag_history import FeatureFlag, FeatureFlagHistory
from devops.models.software_enable_feature_flag import Software, SoftwareEnableFeatureFlag



class ModelHistoryAPI(
    PrimaryModelHistoryAPI,
    TestCase,
):

    audit_model = FeatureFlag

    model = FeatureFlagHistory

    @classmethod
    def setUpTestData(self):

        super().setUpTestData()

        software = Software.objects.create(
            organization = self.organization,
            name = 'one',
        )

        SoftwareEnableFeatureFlag.objects.create(
            organization = self.organization,
            software = software,
            enabled = True
        )

        self.audit_object = self.audit_model.objects.create(
            organization = self.organization,
            name = 'one',
            enabled = True,
            software = software
        )


        self.history_entry = self.model.objects.create(
            organization = self.audit_object.organization,
            action = self.model.Actions.ADD,
            user = self.view_user,
            before = {},
            after = {},
            content_type = ContentType.objects.get(
                app_label = self.audit_object._meta.app_label,
                model = self.audit_object._meta.model_name,
            ),
            model = self.audit_object,
        )


        self.make_request()

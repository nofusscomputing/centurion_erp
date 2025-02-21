from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

from core.tests.abstract.test_unit_model_history_api_v2 import PrimaryModelHistoryAPI

from access.models.organization_history import Organization, OrganizationHistory



class ModelHistoryAPI(
    PrimaryModelHistoryAPI,
    TestCase,
):

    audit_model = Organization

    model = OrganizationHistory

    @classmethod
    def setUpTestData(self):

        super().setUpTestData()

        self.audit_object = self.organization

        self.history_entry = self.model.objects.create(
            organization = self.audit_object,
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

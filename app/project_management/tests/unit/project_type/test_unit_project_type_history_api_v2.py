from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

from project_management.models.project_type_history import ProjectType, ProjectTypeHistory
from core.tests.abstract.test_unit_model_history_api_v2 import PrimaryModelHistoryAPI



class ModelHistoryAPI(
    PrimaryModelHistoryAPI,
    TestCase,
):

    audit_model = ProjectType

    model = ProjectTypeHistory

    @classmethod
    def setUpTestData(self):

        super().setUpTestData()

        self.audit_object = self.audit_model.objects.create(
            organization = self.organization,
            name = 'one',
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

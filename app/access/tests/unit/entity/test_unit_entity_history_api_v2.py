from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

from access.models.entity_history import Entity, EntityHistory

from core.tests.abstract.test_unit_model_history_api_v2 import PrimaryModelHistoryAPI



class ModelHistoryAPITestCases(
    PrimaryModelHistoryAPI,
):
    """ Model Histoy Test Cases

    Test must be setup by creating object `kwargs_create_audit_object` with the
    attributes required to create the object.
    """

    audit_model = None

    kwargs_create_audit_object: dict = {}

    model = EntityHistory

    @classmethod
    def setUpTestData(self):

        super().setUpTestData()

        self.audit_object = self.audit_model.objects.create(
            organization = self.organization,
            entity_type = self.audit_model._meta.model_name,
            **self.kwargs_create_audit_object
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



class EntityModelHistoryAPIInheritedCases(
    ModelHistoryAPITestCases,
):

    audit_model = None

    kwargs_create_audit_object: dict = None


    @classmethod
    def setUpTestData(self):

        self.kwargs_create_audit_object.update(
            super().kwargs_create_audit_object
        )

        super().setUpTestData()



class EntityModelHistoryAPITest(
    ModelHistoryAPITestCases,
    TestCase,
):

    audit_model = Entity

    kwargs_create_audit_object: dict = {}

from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

from core.models.manufacturer_history import Manufacturer, ManufacturerHistory
from core.tests.abstract.test_unit_model_history_api_v2 import BaseModelHistoryAPI



class ModelHistoryAPI(
    BaseModelHistoryAPI,
    TestCase,
):

    audit_model = Manufacturer

    model = ManufacturerHistory

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



    # def test_api_field_exists_model_notes(self):
    #     """ Test for existance of API Field

    #     Test case is a duplicate of a test with the same name.
    #     This model does not have a `model_notes` field.

    #     model_notes field must exist
    #     """

    #     assert 'model_notes' not in self.api_data


    # def test_api_field_type_model_notes(self):
    #     """ Test for type for API Field

    #     Test case is a duplicate of a test with the same name.
    #     This model does not have a `model_notes` field.

    #     model_notes field must be str
    #     """

    #     pass

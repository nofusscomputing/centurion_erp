from django.test import TestCase

from core.tests.abstract.test_functional_history import HistoryEntriesCommon

from settings.models.app_settings_history import AppSettings, AppSettingsHistory



class History(
    HistoryEntriesCommon,
    TestCase,
):

    model = AppSettings

    history_model = AppSettingsHistory


    @classmethod
    def setUpTestData(self):

        super().setUpTestData()

        self.field_name = 'global_organization_id'

        self.field_value_original = self.organization

        self.field_value_changed = self.extra_organization.pk

        self.obj = self.model.objects.get(
            owner_organization = None
        )

        self.obj.global_organization = self.field_value_original

        self.obj.save()

        self.obj_delete = None    # Object is not deleteable

        self.call_the_banners()



    def test_model_history_entry_create(self):
        """ Test model to ensure history entries are made

        This test case is a duplicate of a test with the same name. This
        model does not have the ability to create/delete.

        On object create a history entry with action `ADD` must be created.
        """

        pass


    def test_model_history_entry_delete(self):
        """ Test model to ensure history entries are made

        This test case is a duplicate of a test with the same name. This
        model does not have the ability to create/delete.

        On object delete all history entries must be removed
        """

        pass


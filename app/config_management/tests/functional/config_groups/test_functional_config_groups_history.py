from django.test import TestCase

from config_management.models.config_groups_history import ConfigGroups, ConfigGroupsHistory

from core.tests.abstract.test_functional_history import HistoryEntriesCommon



class History(
    HistoryEntriesCommon,
    TestCase,
):

    model = ConfigGroups

    history_model = ConfigGroupsHistory


    @classmethod
    def setUpTestData(self):

        super().setUpTestData()


        self.obj = self.model.objects.create(
            organization = self.organization,
            name = self.field_value_original
        )

        self.obj_delete = self.model.objects.create(
            organization = self.organization,
            name = self.field_value_delete
        )

        self.call_the_banners()

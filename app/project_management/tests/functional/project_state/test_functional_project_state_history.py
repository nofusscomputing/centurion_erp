from django.test import TestCase

from core.tests.abstract.test_functional_history import HistoryEntriesCommon

from project_management.models.project_state_history import ProjectState, ProjectStateHistory



class History(
    HistoryEntriesCommon,
    TestCase,
):

    model = ProjectState

    history_model = ProjectStateHistory


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

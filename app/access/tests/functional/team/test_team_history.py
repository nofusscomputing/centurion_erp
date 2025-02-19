from django.test import TestCase

from access.models.team_history import Team, TeamHistory

from core.tests.abstract.test_functional_history import HistoryEntriesCommon



class History(
    HistoryEntriesCommon,
    TestCase,
):

    model = Team

    history_model = TeamHistory


    @classmethod
    def setUpTestData(self):

        super().setUpTestData()

        self.field_name = 'team_name'

        self.obj = self.model.objects.create(
            organization = self.organization,
            # name = self.field_value_original,
            team_name = self.field_value_original
        )

        self.obj_delete = self.model.objects.create(
            organization = self.organization,
            name = self.field_value_delete,
        )

        self.call_the_banners()

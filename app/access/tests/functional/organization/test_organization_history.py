from django.test import TestCase

from access.models.organization_history import Organization, OrganizationHistory

from core.tests.abstract.test_functional_history import HistoryEntriesCommon



class History(
    HistoryEntriesCommon,
    TestCase,
):

    model = Organization

    history_model = OrganizationHistory


    @classmethod
    def setUpTestData(self):

        super().setUpTestData()

        self.obj = self.model.objects.create(
            name = self.field_value_original,
        )

        self.obj_delete = self.model.objects.create(
            name = self.field_value_delete,
        )

        self.call_the_banners()

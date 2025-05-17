from django.test import TestCase

from accounting.models.asset_base_history import AssetBase, AssetBaseAuditHistory

from core.tests.abstract.test_functional_history import HistoryEntriesCommon



class History(
    HistoryEntriesCommon,
    TestCase,
):

    model = AssetBase

    history_model = AssetBaseAuditHistory


    @classmethod
    def setUpTestData(self):

        super().setUpTestData()

        self.field_name = 'asset_number'


        self.obj = self.model.objects.create(
            organization = self.organization,
            asset_number = self.field_value_original,
        )

        self.obj_delete = self.model.objects.create(
            organization = self.organization,
            asset_number = self.field_value_delete,

        )

        self.call_the_banners()

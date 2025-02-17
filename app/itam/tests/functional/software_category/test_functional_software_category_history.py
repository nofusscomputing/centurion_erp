from django.test import TestCase

from core.tests.abstract.test_functional_history import HistoryEntriesCommon

from itam.models.software_category_history import SoftwareCategory, SoftwareCategoryHistory



class History(
    HistoryEntriesCommon,
    TestCase,
):

    model = SoftwareCategory

    history_model = SoftwareCategoryHistory


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

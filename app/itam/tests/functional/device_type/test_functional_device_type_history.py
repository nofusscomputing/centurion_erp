from django.test import TestCase

from core.tests.abstract.test_functional_history import HistoryEntriesCommon

from itam.models.device_type_history import DeviceType, DeviceTypeHistory



class History(
    HistoryEntriesCommon,
    TestCase,
):

    model = DeviceType

    history_model = DeviceTypeHistory


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

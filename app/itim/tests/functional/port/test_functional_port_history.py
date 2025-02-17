from django.test import TestCase

from core.tests.abstract.test_functional_history import HistoryEntriesCommon

from itim.models.port_history import Port, PortHistory



class History(
    HistoryEntriesCommon,
    TestCase,
):

    model = Port

    history_model = PortHistory


    @classmethod
    def setUpTestData(self):

        super().setUpTestData()

        self.field_value_original = 22

        self.field_value_delete = 33

        self.field_name = 'number'


        self.obj = self.model.objects.create(
            organization = self.organization,
            number = self.field_value_original
        )

        self.obj_delete = self.model.objects.create(
            organization = self.organization,
            number = self.field_value_delete
        )

        self.call_the_banners()

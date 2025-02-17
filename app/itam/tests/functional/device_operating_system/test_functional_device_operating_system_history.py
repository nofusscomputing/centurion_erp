from django.test import TestCase

from core.tests.abstract.test_functional_history import HistoryEntriesChildModel

from itam.models.device_history import Device, DeviceHistory
from itam.models.device_operating_system_history import DeviceOperatingSystem, DeviceOperatingSystemHistory
from itam.models.operating_system import OperatingSystem, OperatingSystemVersion


class History(
    HistoryEntriesChildModel,
    TestCase,
):

    model = Device

    history_model = DeviceHistory

    child_model = DeviceOperatingSystem

    history_model_child = DeviceOperatingSystemHistory


    @classmethod
    def setUpTestData(self):

        super().setUpTestData()


        self.obj = self.model.objects.create(
            organization = self.organization,
            name = self.field_value_original
        )

        operating_system = OperatingSystem.objects.create(
            organization = self.organization,
            name = 'os name'
        )

        osv = OperatingSystemVersion.objects.create(
            organization = self.organization,
            name = 'os name',
            operating_system = operating_system
        )


        self.obj_child = self.child_model.objects.create(
            organization = self.organization,
            device = self.obj,
            operating_system_version = osv,
        )

        self.obj_delete = self.model.objects.create(
            organization = self.organization,
            name = self.field_value_delete
        )

        self.field_name_child = 'operating_system_version_id'

        self.field_value_child = osv.pk


        self.call_the_banners()

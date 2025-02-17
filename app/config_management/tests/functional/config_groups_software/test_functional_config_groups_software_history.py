from django.test import TestCase

from config_management.models.config_groups_history import ConfigGroups, ConfigGroupsHistory
from config_management.models.config_groups_software_history import ConfigGroupSoftware, ConfigGroupSoftwareHistory

from core.tests.abstract.test_functional_history import HistoryEntriesChildModel

# from itam.models.device_history import Device, DeviceHistory
# from itam.models.device_software_history import DeviceSoftware, DeviceSoftwareHistory
from itam.models.software import Software


class History(
    HistoryEntriesChildModel,
    TestCase,
):

    model = ConfigGroups

    history_model = ConfigGroupsHistory

    child_model = ConfigGroupSoftware

    history_model_child = ConfigGroupSoftwareHistory


    @classmethod
    def setUpTestData(self):

        super().setUpTestData()


        self.obj = self.model.objects.create(
            organization = self.organization,
            name = self.field_value_original
        )

        software = Software.objects.create(
            organization = self.organization,
            name = 'software name'
        )


        self.obj_child = self.child_model.objects.create(
            organization = self.organization,
            config_group = self.obj,
            software = software,
        )

        self.obj_delete = self.model.objects.create(
            organization = self.organization,
            name = self.field_value_delete
        )

        self.field_name_child = 'software_id'

        self.field_value_child = software.pk


        self.call_the_banners()

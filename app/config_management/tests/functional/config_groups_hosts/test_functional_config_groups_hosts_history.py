from django.test import TestCase

from config_management.models.config_groups_history import ConfigGroups, ConfigGroupsHistory
from config_management.models.config_groups_hosts_history import ConfigGroupHosts, ConfigGroupHostsHistory

from core.tests.abstract.test_functional_history import HistoryEntriesChildModel

from itam.models.device import Device



class History(
    HistoryEntriesChildModel,
    TestCase,
):

    model = ConfigGroups

    history_model = ConfigGroupsHistory

    child_model = ConfigGroupHosts

    history_model_child = ConfigGroupHostsHistory


    @classmethod
    def setUpTestData(self):

        super().setUpTestData()


        self.obj = self.model.objects.create(
            organization = self.organization,
            name = self.field_value_original
        )

        device = Device.objects.create(
            organization = self.organization,
            name = 'device name'
        )


        self.obj_child = self.child_model.objects.create(
            organization = self.organization,
            group = self.obj,
            host = device,
        )

        self.obj_delete = self.model.objects.create(
            organization = self.organization,
            name = self.field_value_delete
        )

        self.field_name_child = 'host_id'

        self.field_value_child = device.pk


        self.call_the_banners()

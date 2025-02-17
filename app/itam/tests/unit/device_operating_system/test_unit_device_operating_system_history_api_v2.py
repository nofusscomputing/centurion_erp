from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

from core.tests.abstract.test_unit_model_history_api_v2 import ChildModelHistoryAPI

from itam.models.device import Device
from itam.models.device_operating_system_history import DeviceOperatingSystem, DeviceOperatingSystemHistory
from itam.models.operating_system import OperatingSystem, OperatingSystemVersion


class ModelHistoryAPI(
    ChildModelHistoryAPI,
    TestCase,
):

    audit_model = Device

    audit_model_child = DeviceOperatingSystem

    model = DeviceOperatingSystemHistory

    @classmethod
    def setUpTestData(self):

        super().setUpTestData()

        self.audit_object = self.audit_model.objects.create(
            organization = self.organization,
            name = 'one',
        )

        osv = OperatingSystemVersion.objects.create(
            organization = self.organization,
            name = 'one',
            operating_system = OperatingSystem.objects.create(
                organization = self.organization,
                name = 'one',
            )
        )

        self.audit_object_child = self.audit_model_child.objects.create(
            organization = self.organization,
            device = self.audit_object,
            operating_system_version = osv,
        )


        self.history_entry = self.model.objects.create(
            organization = self.audit_object.organization,
            action = self.model.Actions.ADD,
            user = self.view_user,
            before = {},
            after = {},
            content_type = ContentType.objects.get(
                app_label = self.audit_object._meta.app_label,
                model = self.audit_object._meta.model_name,
            ),
            model = self.audit_object,
            child_model = self.audit_object_child
        )


        self.make_request()

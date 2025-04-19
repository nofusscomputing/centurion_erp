from django.test import TestCase

from access.models.organization import Organization

from app.tests.unit.test_unit_models import (
    TenancyObjectInheritedCases
)

from itam.models.device import Device, DeviceOperatingSystem
from itam.models.operating_system import OperatingSystem, OperatingSystemVersion



class DeviceOperatingSystemModel(
    TenancyObjectInheritedCases,
    TestCase,
):

    model = DeviceOperatingSystem



    @classmethod
    def setUpTestData(self):
        """ Setup Test

        """

        self.organization = Organization.objects.create(name='test_org')


        self.parent_item = Device.objects.create(
            organization = self.organization,
            name = 'device_name'
        )

        os = OperatingSystem.objects.create(
            organization = self.organization,
            name = 'os_name'
        )

        os_version = OperatingSystemVersion.objects.create(
            name = "12",
            operating_system = os,
            organization = self.organization,
        )


        self.kwargs_item_create = {
            'operating_system_version': os_version,
            'device': self.parent_item
        }
        

        super().setUpTestData()



    def test_model_has_property_parent_object(self):
        """ Check if model contains 'parent_object'
        
            This is a required property for all models that have a parent
        """

        assert hasattr(self.model, 'parent_object')


    def test_model_property_parent_object_returns_object(self):
        """ Check if model contains 'parent_object'
        
            This is a required property for all models that have a parent
        """

        assert self.item.parent_object == self.parent_item

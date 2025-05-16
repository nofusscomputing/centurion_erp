from django.test import TestCase

from access.models.tenant import Tenant as Organization

from centurion.tests.unit.test_unit_models import (
    TenancyObjectInheritedCases
)

from itam.models.device import Device, DeviceSoftware
from itam.models.software import Software



class DeviceSoftwareModel(
    TenancyObjectInheritedCases,
    TestCase,
):

    model = DeviceSoftware


    @classmethod
    def setUpTestData(self):
        """ Setup Test

        """

        self.organization = Organization.objects.create(name='test_org')


        self.parent_item = Device.objects.create(
            organization = self.organization,
            name = 'device_name'
        )

        self.software_item = Software.objects.create(
            organization = self.organization,
            name = 'software_name',
        )

        self.kwargs_item_create = {
            'software': self.software_item,
            'device': self.parent_item,
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

from django.test import TestCase

from access.models.tenant import Tenant as Organization

from centurion.tests.unit.test_unit_models import (
    TenancyObjectInheritedCases
)

from config_management.models.groups import ConfigGroups, ConfigGroupSoftware

from itam.models.device import DeviceSoftware
from itam.models.software import Software



class ConfigGroupSoftwareModel(
    TenancyObjectInheritedCases,
    TestCase,
):

    model = ConfigGroupSoftware


    @classmethod
    def setUpTestData(self):
        """ Setup Test

        """

        self.organization = Organization.objects.create(name='test_org')


        self.parent_item = ConfigGroups.objects.create(
            organization = self.organization,
            name = 'group_one'
        )

        self.software_item = Software.objects.create(
            organization = self.organization,
            name = 'softwareone',
        )

        self.kwargs_item_create = {
            'software': self.software_item,
            'config_group': self.parent_item,
            'action': DeviceSoftware.Actions.INSTALL
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

import pytest

from django.test import TestCase

from api.tests.abstract.test_metadata_functional import MetadataAttributesFunctional, MetaDataNavigationEntriesFunctional

from itam.models.device import Device

from itim.models.services import Service, Port



@pytest.mark.model_service
class ViewSetBase(
    MetadataAttributesFunctional,
    MetaDataNavigationEntriesFunctional,
):

    model = Service

    app_namespace = 'v2'
    
    url_name = '_api_service'

    change_data = {'name': 'device-change'}

    delete_data = {}

    @classmethod
    def setUpTestData(self):
        """Setup Test

        1. Create an organization for user and item
        . create an organization that is different to item
        2. Create a team
        3. create teams with each permission: view, add, change, delete
        4. create a user per team
        """

        super().presetUpTestData()

        super().setUpTestData()



        device = Device.objects.create(
            organization=self.organization,
            name = 'device'
        )

        self.global_org_item = self.model.objects.create(
            organization = self.global_organization,
            name = 'global_item',
            device = device,
            config_key_variable = 'value'
        )

        port = Port.objects.create(
            organization=self.organization,
            number = 80,
            protocol = Port.Protocol.TCP
        )

        self.item = self.model.objects.create(
            organization=self.organization,
            name = 'os name',
            device = device,
            config_key_variable = 'value'
        )

        self.other_org_item = self.model.objects.create(
            organization=self.different_organization,
            name = 'os name b',
            device = device,
            config_key_variable = 'values'
        )

        self.item.port.set([ port ])



        self.url_view_kwargs = {'pk': self.item.id}

        self.add_data = {
            'name': 'team-post',
            'organization': self.organization.id,
            'device': device.id,
            'port': [ port.id ],
            'config_key_variable': 'value'
        }



@pytest.mark.module_itim
class ServiceMetadata(
    ViewSetBase,
    TestCase
):

    menu_id = 'itim'

    menu_entry_id = 'service'

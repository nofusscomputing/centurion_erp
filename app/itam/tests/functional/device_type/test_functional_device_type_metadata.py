import pytest

from django.test import TestCase


from api.tests.abstract.test_metadata_functional import MetadataAttributesFunctional

from itam.models.device import DeviceType



@pytest.mark.model_devicemodel
class ViewSetBase:

    model = DeviceType

    app_namespace = 'v2'
    
    url_name = '_api_devicetype'

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


        self.item = self.model.objects.create(
            organization = self.organization,
            name = 'one-add'
        )

        self.other_org_item = self.model.objects.create(
            organization = self.different_organization,
            name = 'two-add'
        )


        self.url_view_kwargs = {'pk': self.item.id}

        self.add_data = {
            'name': 'team-post',
            'organization': self.organization.id,
        }



@pytest.mark.module_itam
class DeviceTypeMetadata(
    ViewSetBase,
    MetadataAttributesFunctional,
    TestCase
):

    pass

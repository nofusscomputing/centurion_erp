import pytest

from django.test import TestCase

from api.tests.abstract.test_metadata_functional import MetadataAttributesFunctional

from itim.models.services import Port



@pytest.mark.model_port
class ViewSetBase(
    MetadataAttributesFunctional,
):

    model = Port

    app_namespace = 'v2'
    
    url_name = '_api_port'

    change_data = {'number': 21}

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

        self.global_org_item = self.model.objects.create(
            organization = self.global_organization,
            number = 8181,
            protocol = Port.Protocol.TCP
        )


        self.item = self.model.objects.create(
            organization = self.organization,
            number = 80,
            protocol = Port.Protocol.TCP
        )

        self.other_org_item = self.model.objects.create(
            organization = self.different_organization,
            number = 81,
            protocol = Port.Protocol.TCP
        )


        self.url_view_kwargs = {'pk': self.item.id}

        self.add_data = {
            'number': 80,
            'protocol': Port.Protocol.TCP,
            'organization': self.organization.id,
        }



@pytest.mark.module_itim
class PortMetadata(
    ViewSetBase,
    TestCase
):

    pass

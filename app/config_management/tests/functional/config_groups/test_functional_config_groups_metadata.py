import pytest

from django.test import TestCase


from api.tests.abstract.test_metadata_functional import MetadataAttributesFunctional, MetaDataNavigationEntriesFunctional

from config_management.models.groups import ConfigGroups




@pytest.mark.model_configgroups
class ViewSetBase:

    model = ConfigGroups

    app_namespace = 'v2'

    url_name = '_api_configgroups'

    change_data = {'name': 'device'}

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

        self.add_data = {
            'name': 'team_post',
            'organization': self.organization.id,
        }

        self.item = self.model.objects.create(
            organization = self.organization,
            name = 'one'
        )

        self.other_org_item = self.model.objects.create(
            organization = self.different_organization,
            name = 'two'
        )

        self.url_view_kwargs = {'pk': self.item.id}



@pytest.mark.module_config_management
class ConfigGroupsMetadata(
    ViewSetBase,
    MetadataAttributesFunctional,
    MetaDataNavigationEntriesFunctional,
    TestCase
):

    menu_id = 'config_management'

    menu_entry_id = 'group'

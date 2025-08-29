import pytest
import django

from django.test import TestCase

from api.tests.abstract.test_metadata_functional import MetadataAttributesFunctional

from config_management.models.groups import ConfigGroups, ConfigGroupSoftware, Software, SoftwareVersion

User = django.contrib.auth.get_user_model()



@pytest.mark.model_configgroupsoftware
class ViewSetBase:

    model = ConfigGroupSoftware

    app_namespace = 'v2'
    
    url_name = '_api_configgroupsoftware'

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


        self.config_group = ConfigGroups.objects.create(
            organization = self.organization,
            name = 'one'
        )

        self.config_group_b = ConfigGroups.objects.create(
            organization = self.different_organization,
            name = 'two'
        )

        self.url_kwargs = { 'config_group_id': self.config_group.id }

        self.software = Software.objects.create(
            organization = self.organization,
            name = 'random name'
        )

        self.software_two = Software.objects.create(
            organization = self.organization,
            name = 'random name two'
        )

        self.software_version = SoftwareVersion.objects.create(
            organization = self.organization,
            software = self.software,
            name = '1.1.1'
        )


        self.software_version_two = SoftwareVersion.objects.create(
            organization = self.organization,
            software = self.software_two,
            name = '2.2.2'
        )


        self.item = self.model.objects.create(
            organization = self.organization,
            config_group = self.config_group,
            software = self.software,
            version = self.software_version
        )

        self.other_org_item = self.model.objects.create(
            organization = self.different_organization,
            config_group = self.config_group_b,
            software = self.software,
            version = self.software_version
        )


        self.url_view_kwargs = {'config_group_id': self.config_group.id, 'pk': self.item.id}

        self.add_data = {
            'organization': self.organization.id,
            'software': self.software_two.id,
            'config_group': self.config_group.id,
            'version': self.software_version_two.id
        }



@pytest.mark.module_config_management
class ConfigGroupSoftwareMetadata(
    ViewSetBase,
    MetadataAttributesFunctional,
    TestCase
):

    pass

import pytest

from django.test import TestCase

from access.models.tenant import Tenant

from api.tests.abstract.test_metadata_functional import MetadataAttributesFunctional

from devops.models.software_enable_feature_flag import SoftwareEnableFeatureFlag

from itam.models.software import Software




@pytest.mark.model_featureflag
class ViewSetBase(
    MetadataAttributesFunctional,
):

    model = SoftwareEnableFeatureFlag

    app_namespace = 'v2'
    
    url_name = '_api_softwareenablefeatureflag'

    change_data = {'enabled': False}

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

        self.add_organization = Tenant.objects.create(name='add_organization')

        super().presetUpTestData()

        super().setUpTestData()

        software = Software.objects.create(
            organization = self.organization,
            name = 'soft',
        )


        self.global_org_item = self.model.objects.create(
            organization = self.global_organization,
            software = software,
            enabled = True
        )


        self.item = self.model.objects.create(
            organization = self.organization,
            software = software,
            enabled = True
        )

        self.url_kwargs = {
            'software_id': software.id,
        }

        self.url_view_kwargs = {
            'software_id': software.id,
            'pk': self.item.id
        }


        self.other_org_item = self.model.objects.create(
            organization = self.different_organization,
            software = software,
            enabled = True
        )


        self.software_add = Software.objects.create(
            organization = self.add_organization,
            name = 'soft add',
        )

        self.add_data = {
            'enabled': True,
            'organization': self.add_organization.id,
            'software': self.software_add.id,
        }



@pytest.mark.module_devops
class Metadata(
    ViewSetBase,
    TestCase
):

    pass

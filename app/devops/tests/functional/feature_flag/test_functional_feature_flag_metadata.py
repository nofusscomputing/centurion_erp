import pytest

from django.test import TestCase

from api.tests.abstract.test_metadata_functional import MetadataAttributesFunctional

from devops.models.feature_flag import FeatureFlag
from devops.models.software_enable_feature_flag import SoftwareEnableFeatureFlag

from itam.models.software import Software



@pytest.mark.model_featureflag
class ViewSetBase(
    MetadataAttributesFunctional,
):

    model = FeatureFlag

    app_namespace = 'v2'

    url_name = 'devops:_api_featureflag'

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

        software = Software.objects.create(
            organization = self.organization,
            name = 'soft',
        )

        SoftwareEnableFeatureFlag.objects.create(
            organization = self.organization,
            software = software,
            enabled = True
        )

        self.global_org_item = self.model.objects.create(
            organization = self.global_organization,
            name = 'global_item',
            software = software,
        )

        self.item = self.model.objects.create(
            organization = self.organization,
            name = 'one',
            software = software,
            description = 'desc',
            model_notes = 'text',
            enabled = True
        )

        self.other_org_item = self.model.objects.create(
            organization = self.different_organization,
            name = 'two',
            software = software,
        )


        self.url_view_kwargs = {'pk': self.item.id}

        self.add_data = {
            'name': 'team_post',
            'organization': self.organization.id,
            'software': software.id,
        }



@pytest.mark.module_devops
class FeatureFlagMetadata(
    ViewSetBase,
    TestCase
):

    pass

import pytest

from django.test import TestCase

from api.tests.abstract.test_metadata_functional import MetadataAttributesFunctional

from itam.models.software import Software, SoftwareVersion



@pytest.mark.model_softwareversion
class ViewSetBase(
    MetadataAttributesFunctional,
):

    model = SoftwareVersion

    app_namespace = 'v2'
    
    url_name = '_api_softwareversion'

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

        software = Software.objects.create(
                organization = self.organization,
                name = 'software'
            )


        self.global_org_item = self.model.objects.create(
            organization = self.global_organization,
            name = '12',
            software = software
        )

        software_b = Software.objects.create(
                organization = self.different_organization,
                name = 'software-b'
            )

        self.item = self.model.objects.create(
            organization = self.organization,
            name = '12',
            software = software
        )

        self.other_org_item = self.model.objects.create(
            organization = self.different_organization,
            name = '13',
            software = software_b
        )


        self.url_view_kwargs = {'software_id': software.id, 'pk': self.item.id}

        self.url_kwargs = {'software_id': software.id}

        self.add_data = {
            'name': 'team-post',
            'organization': self.organization.id,
        }



@pytest.mark.module_itam
class SoftwareVersionMetadata(
    ViewSetBase,
    TestCase
):

    pass

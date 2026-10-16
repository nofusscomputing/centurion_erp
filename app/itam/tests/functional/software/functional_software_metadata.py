import pytest

from django.test import TestCase

from api.tests.abstract.test_metadata_functional import MetadataAttributesFunctional, MetaDataNavigationEntriesFunctional

from itam.models.software import Software



@pytest.mark.model_software
class ViewSetBase(
    MetadataAttributesFunctional,
    MetaDataNavigationEntriesFunctional,
):

    model = Software

    app_namespace = 'v2'

    url_name = '_api_software'

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

        self.global_org_item = self.model.objects.create(
            organization = self.global_organization,
            name = 'global_item'
        )

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
class SoftwareMetadata(
    ViewSetBase,
    TestCase
):

    menu_id = 'itam'

    menu_entry_id = 'software'

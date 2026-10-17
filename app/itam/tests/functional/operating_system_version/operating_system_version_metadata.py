import pytest

from django.test import TestCase

from api.tests.abstract.test_metadata_functional import MetadataAttributesFunctional

from itam.models.operating_system import OperatingSystem, OperatingSystemVersion


@pytest.mark.model_operatingsystemversion
class ViewSetBase(
    MetadataAttributesFunctional,
):

    model = OperatingSystemVersion

    app_namespace = 'v2'

    url_name = '_api_operatingsystemversion'

    change_data = {'name': '22'}

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


        os = OperatingSystem.objects.create(
            organization = self.organization,
            name = 'one-add'
        )


        self.global_org_item = self.model.objects.create(
            organization = self.global_organization,
            name = '22',
            operating_system = os
        )

        os_b = OperatingSystem.objects.create(
            organization = self.different_organization,
            name = 'two-add'
        )


        self.item = self.model.objects.create(
            organization = self.organization,
            name = '5',
            operating_system = os
        )

        self.other_org_item = self.model.objects.create(
            organization = self.different_organization,
            name = '6',
            operating_system = os_b
        )


        self.url_view_kwargs = {'operating_system_id': os.id, 'pk': self.item.id}

        self.url_kwargs = {'operating_system_id': os.id,}

        self.add_data = {
            'name': '22',
            'organization': self.organization.id,
        }



@pytest.mark.module_itam
class OperatingSystemVersionMetadata(
    ViewSetBase,
    TestCase
):

    pass

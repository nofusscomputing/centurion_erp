import pytest

from django.test import TestCase

from api.tests.abstract.test_metadata_functional import (
    MetadataAttributesFunctionalBase,
    MetadataAttributesFunctionalEndpoint
)

from settings.models.app_settings import AppSettings



@pytest.mark.model_appsettings
class ViewSetBase(
    MetadataAttributesFunctionalEndpoint,
    MetadataAttributesFunctionalBase,
):

    model = AppSettings

    app_namespace = 'v2'
    
    url_name = '_api_appsettings'

    change_data = {'device_model_is_global': True}

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

        self.item = AppSettings.objects.get( id = 1 )

        self.item.global_organization = self.organization

        self.item.save()


        self.url_view_kwargs = {'pk': self.item.id}

        self.add_data = {
            'name': 'team-post',
            'organization': self.organization.id,
        }



@pytest.mark.module_settings
class AppSettingsMetadata(
    ViewSetBase,
    TestCase
):

    viewset_type = 'detail'

    @classmethod
    def setUpTestData(self):

        super().setUpTestData()

        self.url_kwargs = self.url_view_kwargs

        self.view_user.is_superuser = True
        self.view_user.save()


import pytest

from django.test import TestCase

from api.tests.abstract.test_metadata_functional import (
    MetadataAttributesFunctionalEndpoint,
    MetadataAttributesFunctionalBase,
)


from settings.models.user_settings import UserSettings



@pytest.mark.functional
@pytest.mark.module_settings
class ViewSetBase(
    MetadataAttributesFunctionalEndpoint,
    MetadataAttributesFunctionalBase,
):

    model = UserSettings

    app_namespace = 'v2'

    url_name = '_api_usersettings'

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

        self.item = self.model.objects.get( id = self.view_user.id )

        self.item.default_organization = self.organization

        self.item.save()


        self.url_view_kwargs = {'pk': self.item.id}

        self.add_data = {
            'name': 'team-post',
            'organization': self.organization.id,
        }



@pytest.mark.model_usersettings
class UserSettingsMetadata(
    ViewSetBase,
    TestCase
):

    viewset_type = 'detail'

    @classmethod
    def setUpTestData(self):

        super().setUpTestData()

        self.url_kwargs = self.url_view_kwargs

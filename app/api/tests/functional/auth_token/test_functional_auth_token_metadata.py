import pytest

from django.test import TestCase

from api.models.tokens import AuthToken

from api.tests.abstract.test_metadata_functional import (
    MetadataAttributesFunctionalEndpoint,
    MetadataAttributesFunctionalBase,
)


@pytest.mark.model_authtoken
class ViewSetBase(
    MetadataAttributesFunctionalEndpoint,
    MetadataAttributesFunctionalBase,
):

    model = AuthToken

    app_namespace = 'v2'
    
    url_name = '_api_authtoken'

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

        self.item = self.model.objects.create(
            note = 'a note',
            token = self.model().generate,
            user = self.view_user,
            expires = '2025-02-25T23:14Z'
        )

        self.item_delete = self.model.objects.create(
            note = 'a note',
            token = self.model().generate,
            user = self.delete_user,
            expires = '2025-02-25T23:14Z'
        )


        self.url_view_kwargs = {
            'model_id': self.view_user.id,
            'pk': self.item.id,
        }

        self.url_kwargs = {
            'model_id': self.view_user.id,
        }

        self.add_data = {
            'note': 'a note',
            'token': self.model().generate,
            'expires': '2025-02-26T23:14Z'
        }



@pytest.mark.module_api
class Metadata(
    ViewSetBase,
    TestCase
):

    viewset_type = 'detail'

    @classmethod
    def setUpTestData(self):

        super().setUpTestData()

        self.url_kwargs = self.url_view_kwargs
